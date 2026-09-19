# mri-research — a Claude skill for MRI reconstruction research

Turn Claude into a fluent MRI reconstruction research assistant: a curated,
**verified reference hub** for MR physics, reconstruction methods, software
tools, raw-data formats, datasets, pulse-sequence & trajectory design, MRI
hardware, and programmatic literature access.

This is a **pointer / reference skill**, not a data dump. MR datasets are
hundreds of GB to multiple TB and are governed by data-use agreements, and
textbooks are copyrighted — so the skill teaches Claude *where the
authoritative resources live* and *which tool fits a given task*, and links out
to the community's own repos, papers, courses, and datasets rather than
bundling them.

It is built **on top of, and in credit to,** the open MRI community — the
Lustig (UC Berkeley) and Pauly (Stanford) lineage, the BART / SigPy / ISMRMRD /
Gadgetron / Pulseq ecosystems, the fastMRI and mridata.org efforts, ISMRM, and
the many awesome-list maintainers. All primary work belongs to its authors;
this skill is a navigation layer that helps you reach them faster.

## What's inside

- `SKILL.md` — the navigator: a core MR mental model, ground rules, and a
  routing table from question → reference file.
- `references/foundations.md` — MR physics, k-space, and where to learn
  (Berkeley EE225E, Stanford EE369B/C, Hornak, Elster/MRIquestions, ISMRM).
- `references/recon-methods.md` — the landmark-paper reading list: parallel
  imaging (SENSE/GRAPPA/ESPIRiT/SPIRiT), compressed sensing, low-rank, deep
  learning (VarNet/MoDL/E2E-VarNet), and diffusion / score-based recon (with
  codebases), plus a "which method for which task" guide.
- `references/tools.md` — which toolbox to use and how: BART, SigPy, MIRT.jl,
  MRIReco.jl, torchkbnufft, gpuNUFFT, DIRECT, fastMRI, Gadgetron.
- `references/data-and-formats.md` — ISMRMRD and vendor raw formats (Siemens
  twix, GE P-file, Philips raw), converters, and open datasets.
- `references/sequences-and-trajectories.md` — pulse-sequence programming
  (Pulseq/PyPulseq, vendor SDKs), trajectory design, and simulation (KomaMRI).
- `references/hardware.md` — MRI hardware and the open-hardware community
  (OSI², MaRCoS, OCRA, low-field, coils, gradients, safety).
- `references/literature-access.md` — APIs, API keys, and MCP servers for
  finding papers/data (arXiv, PubMed, Semantic Scholar, OpenAlex, Crossref).
- `references/radiology-primer.md` — how MR image contrast reads (T1/T2/FLAIR/
  DWI), scoped strictly as background orientation.

## Install

**Claude Code (personal skill):**

```bash
git clone https://github.com/KeWang0622/mri-research-skill ~/.claude/skills/mri-research
```

Claude Code auto-discovers skills in `~/.claude/skills/`. The skill's
invocation name comes from the `name:` field in `SKILL.md` (`mri-research`),
so the folder name is flexible — cloning into `~/.claude/skills/mri-research`
just keeps things tidy. For a project-scoped install, clone into
`.claude/skills/` inside your repository instead.

## Scope & disclaimers

- **Radiology reading is orientation, not diagnosis.** The reading primer helps
  you follow research conversations about image contrast; it is explicitly not
  clinical or diagnostic advice. Interpretation of real scans belongs to a
  qualified radiologist.
- **Respect dataset licenses.** fastMRI requires a signed data-use agreement;
  mridata.org datasets carry per-dataset terms. The skill never helps
  circumvent an access gate.
- **Links can rot.** Every link was verified when written, but repos move and
  course pages change each semester; the skill instructs Claude to confirm
  load-bearing links before acting on them.

## Contributing

The field moves fast. Issues and PRs that add landmark papers, new toolboxes,
corrected links, or additional vendor/format notes are welcome. Please keep the
pointer-not-dump philosophy: link and summarize, don't vendor datasets or
copyrighted text.

## License

No license file is included yet — until one is added, default copyright applies
(all rights reserved). If you intend this for open community use, add a
permissive license (e.g., MIT or CC BY 4.0) to make reuse unambiguous.
