<h1 align="center">mri-research</h1>

<p align="center">
  <strong>A Claude skill that turns Claude into a fluent MRI reconstruction research assistant.</strong><br>
  A curated, verified reference hub for MR physics, reconstruction methods, tools, datasets, sequences, and hardware.
</p>

<p align="center">
  <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg">
  <img alt="Claude Code Skill" src="https://img.shields.io/badge/Claude%20Code-Skill-8A2BE2">
  <img alt="Domain: MRI reconstruction" src="https://img.shields.io/badge/domain-MRI%20reconstruction-1f6feb">
  <img alt="Status: v0.1.0" src="https://img.shields.io/badge/status-v0.1.0-brightgreen">
  <img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg">
</p>

---

## Contents

- [What it is](#what-it-is)
- [Why it exists](#why-it-exists)
- [What's inside](#whats-inside)
- [Install](#install)
- [Example prompts](#example-prompts)
- [Design principles](#design-principles)
- [Scope & disclaimers](#scope--disclaimers)
- [Contributing](#contributing)
- [Citing](#citing)
- [Acknowledgements](#acknowledgements)
- [License](#license)

## What it is

`mri-research` is a [Claude](https://claude.com/claude-code) **skill** — a
packaged set of instructions and curated references that Claude loads when a
conversation turns to magnetic resonance imaging. Once installed, Claude can
immediately reason about k-space, pick the right reconstruction method and
toolbox for a task, tell Siemens *twix* from a GE *P-file*, and point you to the
canonical paper, course, dataset, or repository — with verified links.

It is a **pointer / reference skill**, not a data dump. MR datasets run from
hundreds of GB to multiple TB and are governed by data-use agreements, and
textbooks are copyrighted — so the skill teaches Claude *where the authoritative
resources live* and *which tool fits a given task*, and links out to the
community's own repositories, papers, courses, and datasets.

## Why it exists

Getting a coding agent genuinely useful for MRI reconstruction research usually
means re-explaining the same landscape every session: which of a dozen
toolboxes to use, what the landmark papers are, how a vendor raw file is laid
out, where an open dataset lives and under what license. This skill encodes
that orientation once, as a navigable, verified map of the field, so Claude
starts every MR conversation already fluent and pointing at primary sources —
a professional starting point that builds **on top of** the open MRI community
rather than duplicating it.

## What's inside

| File | Covers |
|---|---|
| [`SKILL.md`](SKILL.md) | Navigator: core MR mental model, ground rules, and a question → reference routing table |
| [`references/foundations.md`](references/foundations.md) | MR physics / k-space and where to learn (Berkeley EE225E, Stanford EE369B/C, Hornak, MRIquestions, ISMRM) |
| [`references/recon-methods.md`](references/recon-methods.md) | Landmark-paper reading list: parallel imaging, compressed sensing, low-rank & dynamic, deep learning, diffusion/score-based, MR fingerprinting — with a "which method for which task" guide |
| [`references/tools.md`](references/tools.md) | Toolbox decision guide + usage patterns: BART, SigPy, MIRT.jl, MRIReco.jl, torchkbnufft, gpuNUFFT, mri-nufft, pygrappa, DIRECT, fastMRI, DeepInPy, TensorFlow MRI, Gadgetron |
| [`references/data-and-formats.md`](references/data-and-formats.md) | ISMRMRD & vendor raw (Siemens twix, GE P-file, Philips raw), converters, and open datasets (fastMRI, mridata.org, OCMR, SKM-TEA, Calgary-Campinas, CMRxRecon, M4Raw) |
| [`references/sequences-and-trajectories.md`](references/sequences-and-trajectories.md) | Pulse-sequence programming (Pulseq/PyPulseq, vendor SDKs), trajectory design, simulation (KomaMRI) |
| [`references/hardware.md`](references/hardware.md) | MRI hardware and the open-hardware community (OSI², MaRCoS, OCRA, low-field, coils, gradients, safety) |
| [`references/literature-access.md`](references/literature-access.md) | Literature/data APIs, API-key handling, and paper-search MCP servers (arXiv, PubMed, Semantic Scholar, OpenAlex, Crossref) |
| [`references/radiology-primer.md`](references/radiology-primer.md) | MR image-contrast orientation (T1/T2/FLAIR/DWI) — non-diagnostic background only |

## Install

**Claude Code (personal skill):**

```bash
git clone https://github.com/KeWang0622/mri-research-skill ~/.claude/skills/mri-research
```

Claude Code auto-discovers skills in `~/.claude/skills/`. The skill's invocation
name comes from the `name:` field in `SKILL.md` (`mri-research`), so the folder
name is flexible — cloning into `~/.claude/skills/mri-research` just keeps things
tidy.

**Project-scoped install** (share it with a repo's collaborators):

```bash
git clone https://github.com/KeWang0622/mri-research-skill .claude/skills/mri-research
```

No dependencies to install — the skill is Markdown. It will use whatever tools
your Claude session already has (e.g., web search, `gh`, or a paper-search MCP
server) when it needs to fetch or verify something live.

## Example prompts

Once installed, try:

- *"I have 8-channel knee k-space undersampled 4×. Walk me through a PI+CS
  reconstruction and give me the BART commands."*
- *"What's the canonical paper for ESPIRiT, and how is it different from
  SENSE and GRAPPA?"*
- *"I was handed a `meas.dat` file. What is it and how do I get it into
  something I can reconstruct in Python?"*
- *"Design a golden-angle radial gradient-echo sequence in PyPulseq and
  simulate it before I book scanner time."*
- *"Which open dataset should I use to benchmark a cardiac cine reconstruction,
  and what are the access terms?"*
- *"Summarize the current state of diffusion-model MRI reconstruction and point
  me to codebases."*

## Design principles

- **Point, don't vendor.** Link and summarize; never bundle datasets or
  copyrighted text.
- **Primary sources first.** Cite the original paper/repo; use awesome-lists as
  living indexes.
- **Decide, don't just enumerate.** Reference files are organized to help a
  researcher choose the right method/tool.
- **Verify load-bearing links.** Links rot; the skill instructs Claude to
  confirm a link before acting on it.

## Scope & disclaimers

- **Radiology reading is orientation, not diagnosis.** The reading primer helps
  Claude follow research conversations about image contrast; it is explicitly
  not clinical or diagnostic advice. Interpretation of real scans belongs to a
  qualified radiologist.
- **Respect dataset licenses.** fastMRI requires a signed data-use agreement;
  mridata.org datasets carry per-dataset terms. The skill never helps
  circumvent an access gate.
- **Links can rot.** Every link was verified at release, but repositories move
  and course pages change each semester.

## Contributing

Issues and PRs are welcome — see [`CONTRIBUTING.md`](CONTRIBUTING.md). The one
firm rule: preserve the pointer-not-dump philosophy and verify every link and
citation you add.

## Citing

If this skill helps your research or tooling, please cite it via the
[`CITATION.cff`](CITATION.cff) metadata (GitHub's "Cite this repository" button
will format it for you).

## Acknowledgements

This skill is a navigation layer built **on top of, and in credit to,** the open
MRI community — among them the Lustig group (UC Berkeley) and the Pauly/Nishimura
lineage (Stanford); the BART, SigPy, ISMRMRD, Gadgetron, and Pulseq ecosystems;
the fastMRI, mridata.org, OCMR, SKM-TEA, Calgary-Campinas, and CMRxRecon dataset
efforts; the [ISMRM](https://www.ismrm.org); and the maintainers of the
community awesome-lists. All primary work belongs to its respective authors.

## License

Released under the [MIT License](LICENSE). Note that the **external resources**
this skill links to (papers, datasets, software) are governed by their own
licenses and terms — always check them before use.
