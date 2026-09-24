"""Check preservation and opt-in behavior of the project notebook initializer."""
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[2] / 'skills/mri-research/scripts/init_research_memory.py'
spec = importlib.util.spec_from_file_location('memory', SCRIPT)
memory = importlib.util.module_from_spec(spec)
spec.loader.exec_module(memory)


class MemoryTests(unittest.TestCase):
    def test_preserves_notes_and_agent_instructions_on_repeated_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ('AGENTS.md', 'CLAUDE.md'):
                (root / name).write_text('Existing project instructions.\n')
            memory.initialize(root, True)
            (root / '.mri-research/lessons.md').write_text('Evidence from a real experiment.\n')
            before = {p: p.read_bytes() for p in root.rglob('*') if p.is_file()}
            memory.initialize(root, True)
            self.assertEqual(before, {p: p.read_bytes() for p in root.rglob('*') if p.is_file()})
            for name in ('AGENTS.md', 'CLAUDE.md'):
                self.assertTrue((root / name).read_text().startswith('Existing project instructions.\n'))

    def test_private_default_without_agent_file_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            memory.initialize(root)
            self.assertFalse((root / 'AGENTS.md').exists())
            self.assertFalse((root / 'CLAUDE.md').exists())
            subprocess.run(['git', 'init', '-q', tmp], check=True)
            result = subprocess.run(['git', 'check-ignore', '-q', '.mri-research/preferences.md'], cwd=root)
            self.assertEqual(result.returncode, 0)

    def test_does_not_write_through_symlinked_memory(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as other:
            root = Path(tmp)
            (root / '.mri-research').symlink_to(other, target_is_directory=True)
            with self.assertRaises(ValueError):
                memory.initialize(root)
            self.assertEqual(list(Path(other).iterdir()), [])


if __name__ == '__main__':
    unittest.main()
