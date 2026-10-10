"""Behavioral checks for private MRFoundry notebook creation and migration."""
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[2] / 'skills/mri-research/scripts/init_research_memory.py'
spec = importlib.util.spec_from_file_location('memory', SCRIPT)
memory = importlib.util.module_from_spec(spec)
spec.loader.exec_module(memory)
LEGACY_ENTRY = memory.ENTRY.replace('mrfoundry', 'mri-research').replace('MRFoundry', 'MRI')


def git(root, *args):
    return subprocess.run(['git', '-C', str(root), *args], check=True,
                          capture_output=True, text=True)


class MemoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        # macOS's tempfile prefix may itself use the system /var -> /private/var alias.
        self.root = Path(self.tmp.name).resolve()

    def snapshot(self):
        return {str(p.relative_to(self.root)): p.read_bytes()
                for p in self.root.rglob('*') if p.is_file() and not p.is_symlink()}

    def test_fresh_private_creation_and_no_unmanaged_entrypoint_edits(self):
        custom = b'Existing project instructions.\r\nDo not replace me.\r\n'
        (self.root / 'AGENTS.md').write_bytes(custom)
        memory.initialize(self.root)
        notebook = self.root / '.mrfoundry'
        self.assertTrue((notebook / 'runs').is_dir())
        self.assertTrue((notebook / 'INDEX.md').is_file())
        self.assertFalse((self.root / '.mri-research').exists())
        self.assertEqual((self.root / 'AGENTS.md').read_bytes(), custom)
        self.assertFalse((self.root / 'CLAUDE.md').exists())
        git(self.root, 'init', '-q')
        # Even if initialization precedes git init, the notebook's own ignore applies.
        git(self.root, 'check-ignore', '-q', '.mrfoundry/preferences.md')

    def test_repeated_runs_preserve_notes_and_agent_instructions(self):
        for name in ('AGENTS.md', 'CLAUDE.md'):
            (self.root / name).write_bytes(b'Existing project instructions.\r\n')
        git(self.root, 'init', '-q')
        memory.initialize(self.root, True)
        (self.root / '.mrfoundry/lessons.md').write_bytes(b'Evidence from an experiment.\x00\r\n')
        before = self.snapshot()
        self.assertEqual(memory.initialize(self.root, True), [])
        self.assertEqual(before, self.snapshot())
        for name in ('AGENTS.md', 'CLAUDE.md'):
            self.assertTrue((self.root / name).read_bytes().startswith(b'Existing project instructions.\r\n'))
            self.assertEqual((self.root / name).read_text().count(memory.START), 1)

    def test_legacy_migration_preserves_all_existing_bytes_and_relative_links(self):
        notebook = self.root / '.mri-research'
        (notebook / 'runs').mkdir(parents=True)
        notes = {
            'INDEX.md': b'[record](runs/session.md)\r\n',
            'lessons.md': b'Private evidence: \xff\x00\r\n',
            'runs/session.md': b'Existing run\n',
            '.gitignore': b'*\r\n',
        }
        for name, value in notes.items():
            (notebook / name).write_bytes(value)
        memory.initialize(self.root)
        self.assertFalse(notebook.exists())
        for name, value in notes.items():
            self.assertEqual((self.root / '.mrfoundry' / name).read_bytes(), value)
        self.assertTrue((self.root / '.mrfoundry/preferences.md').is_file())
        self.assertEqual(memory.initialize(self.root), [])

    def test_existing_managed_entries_upgrade_without_add_flag(self):
        (self.root / '.mri-research').mkdir()
        prefix, suffix = b'Unrelated instructions.\r\n\n', b'\r\nOther instructions.\xff\n'
        for name in ('AGENTS.md', 'CLAUDE.md'):
            (self.root / name).write_bytes(prefix + LEGACY_ENTRY.rstrip('\n').encode() + suffix)
        memory.initialize(self.root)
        for name in ('AGENTS.md', 'CLAUDE.md'):
            result = (self.root / name).read_bytes()
            self.assertEqual(result, prefix + memory.ENTRY.rstrip('\n').encode() + suffix)
        self.assertEqual(memory.initialize(self.root), [])

    def test_duplicate_old_and_new_managed_entries_collapse_in_place(self):
        separator = b'\nInstructions between managed blocks.\n'
        path = self.root / 'CLAUDE.md'
        path.write_bytes(b'Before\n' + LEGACY_ENTRY.encode() + separator + memory.ENTRY.encode() + b'After\n')
        memory.initialize(self.root, True)
        result = path.read_bytes()
        self.assertEqual(result.count(memory.START.encode()), 1)
        self.assertNotIn(b'mri-research:project-memory', result)
        self.assertIn(separator, result)
        self.assertTrue(result.startswith(b'Before\n'))
        self.assertTrue(result.endswith(b'After\n'))
        self.assertEqual(memory.initialize(self.root, True), [])

    def test_conflicting_directories_leave_everything_unchanged(self):
        for name in ('.mrfoundry', '.mri-research'):
            (self.root / name).mkdir()
            (self.root / name / 'lessons.md').write_text(name)
        (self.root / 'AGENTS.md').write_text(LEGACY_ENTRY)
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, 'Both .mrfoundry and .mri-research exist'):
            memory.initialize(self.root, True)
        self.assertEqual(before, self.snapshot())

    def test_invalid_agent_block_is_detected_before_any_migration_or_write(self):
        (self.root / '.mri-research').mkdir()
        (self.root / '.mri-research/lessons.md').write_text('Evidence')
        (self.root / 'AGENTS.md').write_text(LEGACY_ENTRY)
        (self.root / 'CLAUDE.md').write_text(memory.START)
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, 'Incomplete or nested'):
            memory.initialize(self.root, True)
        self.assertEqual(before, self.snapshot())
        self.assertTrue((self.root / '.mri-research').exists())
        self.assertFalse((self.root / '.mrfoundry').exists())

    def test_nested_or_mismatched_markers_are_rejected(self):
        for bad in (memory.END, memory.START + memory.START + memory.END,
                    memory.START + LEGACY_ENTRY.splitlines()[-1]):
            with self.subTest(block=bad):
                (self.root / 'AGENTS.md').write_text(bad)
                with self.assertRaises(ValueError):
                    memory.initialize(self.root, True)
                self.assertFalse((self.root / '.mrfoundry').exists())

    def test_memory_directory_symlinks_including_dangling_links_are_rejected(self):
        target = self.root / 'elsewhere'
        for name in ('.mrfoundry', '.mri-research'):
            for dangling in (True, False):
                with self.subTest(name=name, dangling=dangling):
                    if not dangling:
                        target.mkdir(exist_ok=True)
                    link = self.root / name
                    link.symlink_to(target, target_is_directory=True)
                    with self.assertRaisesRegex(ValueError, 'symlink'):
                        memory.initialize(self.root)
                    link.unlink()
                    if target.exists():
                        self.assertEqual(list(target.iterdir()), [])
                        target.rmdir()

    def test_symlinked_root_and_ancestor_are_rejected(self):
        actual = self.root / 'actual'
        project = actual / 'project'
        project.mkdir(parents=True)
        alias = self.root / 'alias'
        alias.symlink_to(actual, target_is_directory=True)
        for path in (alias, alias / 'project', alias / '..' / 'actual' / 'project'):
            with self.subTest(path=path):
                with self.assertRaisesRegex(ValueError, 'symlink'):
                    memory.initialize(path)
        self.assertEqual(list(project.iterdir()), [])

    def test_internal_symlinks_refuse_migration_without_touching_targets(self):
        for name in ('INDEX.md', 'runs', 'nested/lesson.md'):
            with self.subTest(name=name):
                notebook = self.root / '.mri-research'
                notebook.mkdir(exist_ok=True)
                link = notebook / name
                link.parent.mkdir(parents=True, exist_ok=True)
                target = self.root / 'target'
                target.write_bytes(b'External content')
                link.symlink_to(target)
                with self.assertRaisesRegex(ValueError, 'symlink'):
                    memory.initialize(self.root)
                self.assertEqual(target.read_bytes(), b'External content')
                self.assertFalse((self.root / '.mrfoundry').exists())
                link.unlink()

    def test_symlinked_agent_entrypoints_are_not_followed(self):
        target = self.root / 'instructions'
        target.write_text('External instructions')
        (self.root / 'CLAUDE.md').symlink_to(target)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            memory.initialize(self.root, True)
        self.assertEqual(target.read_text(), 'External instructions')
        self.assertFalse((self.root / '.mrfoundry').exists())
        self.assertFalse((self.root / 'AGENTS.md').exists())

    def test_file_type_conflicts_are_preflighted(self):
        for name in ('INDEX.md', 'runs'):
            with self.subTest(name=name):
                notebook = self.root / '.mri-research'
                notebook.mkdir(exist_ok=True)
                path = notebook / name
                path.mkdir() if name == 'INDEX.md' else path.write_text('not a directory')
                with self.assertRaises(ValueError):
                    memory.initialize(self.root, True)
                self.assertTrue(notebook.exists())
                self.assertFalse((self.root / '.mrfoundry').exists())
                self.assertFalse((self.root / 'AGENTS.md').exists())
                path.rmdir() if path.is_dir() else path.unlink()

    def test_git_excludes_cover_both_names_and_preserve_existing_content(self):
        git(self.root, 'init', '-q')
        path = self.root / '.git/info/exclude'
        prefix = b'# Local rules\r\nprivate-data/\r\n# no final newline'
        path.write_bytes(prefix)
        memory.initialize(self.root)
        self.assertTrue(path.read_bytes().startswith(prefix + b'\n'))
        for name in ('.mrfoundry', '.mri-research'):
            git(self.root, 'check-ignore', '-q', name + '/future.md')
        before = path.read_bytes()
        memory.initialize(self.root)
        self.assertEqual(path.read_bytes(), before)

    def test_nested_project_uses_repository_local_excludes(self):
        git(self.root, 'init', '-q')
        project = self.root / 'study'
        project.mkdir()
        memory.initialize(project)
        for name in ('.mrfoundry', '.mri-research'):
            git(self.root, 'check-ignore', '-q', 'study/' + name + '/future.md')

    def test_migrating_tracked_legacy_notes_preserves_git_index_and_history(self):
        git(self.root, 'init', '-q')
        legacy = self.root / '.mri-research'
        legacy.mkdir()
        evidence = b'Previously committed research evidence.\r\n'
        (legacy / 'lessons.md').write_bytes(evidence)
        git(self.root, 'add', '.mri-research/lessons.md')
        git(self.root, '-c', 'user.name=Memory test', '-c', 'user.email=test@example.invalid',
            'commit', '-q', '-m', 'Existing tracked notebook')
        history = git(self.root, 'log', '--format=%H').stdout
        index = (self.root / '.git/index').read_bytes()

        memory.initialize(self.root)

        self.assertEqual((self.root / '.git/index').read_bytes(), index)
        self.assertEqual(git(self.root, 'log', '--format=%H').stdout, history)
        self.assertEqual((self.root / '.mrfoundry/lessons.md').read_bytes(), evidence)
        self.assertFalse(legacy.exists())
        self.assertEqual(git(self.root, 'ls-files').stdout, '.mri-research/lessons.md\n')
        self.assertEqual(git(self.root, 'diff', '--cached', '--name-status').stdout, '')
        self.assertEqual(git(self.root, 'status', '--porcelain').stdout,
                         ' D .mri-research/lessons.md\n')
        git(self.root, 'check-ignore', '-q', '.mrfoundry/lessons.md')

    def test_linked_worktree_uses_common_git_excludes(self):
        repo, worktree = self.root / 'repo', self.root / 'worktree'
        repo.mkdir()
        git(repo, 'init', '-q')
        git(repo, '-c', 'user.name=Memory test', '-c', 'user.email=test@example.invalid',
            'commit', '-q', '--allow-empty', '-m', 'Test fixture')
        git(repo, 'worktree', 'add', '-q', '-b', 'memory-test', str(worktree))
        memory.initialize(worktree)
        self.assertTrue((worktree / '.git').is_file())
        for name in ('.mrfoundry', '.mri-research'):
            git(worktree, 'check-ignore', '-q', name + '/future.md')
        self.assertIn(b'.mrfoundry/', (repo / '.git/info/exclude').read_bytes())

    def test_symlinked_git_exclude_or_ancestor_prevents_any_migration(self):
        git(self.root, 'init', '-q')
        (self.root / '.mri-research').mkdir()
        outside = self.root / 'outside'
        outside.mkdir()
        (outside / 'exclude').write_text('Outside ignore rules\n')
        git_info = self.root / '.git/info'
        (git_info / 'exclude').unlink()
        for ancestor in (False, True):
            with self.subTest(ancestor=ancestor):
                if ancestor:
                    git_info.rmdir()
                    git_info.symlink_to(outside, target_is_directory=True)
                else:
                    (git_info / 'exclude').symlink_to(outside / 'exclude')
                with self.assertRaisesRegex(ValueError, 'symlink'):
                    memory.initialize(self.root, True)
                self.assertEqual((outside / 'exclude').read_text(), 'Outside ignore rules\n')
                self.assertTrue((self.root / '.mri-research').exists())
                self.assertFalse((self.root / '.mrfoundry').exists())
                self.assertFalse((self.root / 'AGENTS.md').exists())
                if not ancestor:
                    (git_info / 'exclude').unlink()


if __name__ == '__main__':
    unittest.main()
