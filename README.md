<h1 align="center">MRI Research</h1>

<p align="center">
  <strong>A curated, verified knowledge hub for magnetic resonance imaging research — built for AI agents.</strong><br>
  <a href="skills/mri-research/references/foundations.md">Physics</a> · <a href="skills/mri-research/references/sequences-and-trajectories.md">acquisition</a> · <a href="skills/mri-research/references/recon-methods.md">reconstruction</a> · <a href="skills/mri-research/references/analysis-processing.md">analysis</a> · <a href="skills/mri-research/references/quantitative-and-spectroscopy.md">quantitative MRI</a> · <a href="skills/mri-research/references/quantitative-and-spectroscopy.md">spectroscopy</a> · <a href="skills/mri-research/references/hardware.md">hardware</a>.<br>
  One command makes any AI agent fluent in MRI — so the field's knowledge is open to everyone.
</p>

<p align="center">
  <a href="https://github.com/KeWang0622/mri-research-skill/blob/main/LICENSE"><img alt="License: MIT" src="https://img.shields.io/github/license/KeWang0622/mri-research-skill?style=for-the-badge&labelColor=000000"></a>
  <img alt="Version" src="https://img.shields.io/badge/version-0.3.0-1f6feb?style=for-the-badge&labelColor=000000">
  <img alt="Install: npx skills add" src="https://img.shields.io/badge/install-npx%20skills%20add-000000?style=for-the-badge">
  <a href="https://github.com/KeWang0622/mri-research-skill/stargazers"><img alt="Stars" src="https://img.shields.io/github/stars/KeWang0622/mri-research-skill?style=for-the-badge&labelColor=000000"></a>
</p>

---

## Install

Using the open [`skills`](https://github.com/vercel-labs/skills) CLI — works across Claude Code, Codex, Cursor, OpenCode, and many more agents:

```bash
npx skills add KeWang0622/mri-research-skill
```

<details>
<summary>More install options</summary>

```bash
# Install globally (user directory) instead of the current project
npx skills add KeWang0622/mri-research-skill -g

# Target a specific agent
npx skills add KeWang0622/mri-research-skill -a claude-code

# List what's in the repo without installing
npx skills add KeWang0622/mri-research-skill --list

# Try it without installing — pipe a generated prompt straight into an agent
npx skills use KeWang0622/mri-research-skill | claude
```

Or add it manually by copying `skills/mri-research/` into your agent's skills
directory (e.g., `~/.claude/skills/`). No dependencies — it's Markdown.
</details>

## What it is

A fluent, well-oriented guide to the **whole MRI pipeline** — from spins to
statistics. It's a **pointer / reference** hub, not a data dump: MRI datasets
run from hundreds of GB to multiple TB and sit behind data-use agreements, and
textbooks are copyrighted, so it teaches *where the authoritative resources
live* and *which tool fits a given task*, then links out to the community's own
repositories, papers, courses, and datasets.

Once installed, your agent can immediately reason about k-space, pick the right
reconstruction method and toolbox, tell Siemens *twix* from a GE *P-file*,
preprocess an fMRI dataset with fMRIPrep, or point you to the canonical paper,
course, handbook, or dataset — with verified links.

It builds **on top of, and in credit to,** the open MRI community.

## Why it exists

Built for **AI agents**. MRI expertise is scattered — across papers, course
notes, vendor manuals, and dozens of toolboxes — which makes it slow even for
experts and daunting for newcomers. This packages that landscape into a form an
agent can use directly, so any researcher's agent starts already fluent in MRI.

The goal is simple: **make the MRI community's collective knowledge accessible
to everyone**, through whatever AI agent they already use — an open,
community-maintained starting point rather than know-how locked inside
individual labs.

## The MRI pipeline it maps

```mermaid
flowchart LR
  P[Physics and k-space] --> ACQ[Acquisition - sequences, trajectories, RF]
  ACQ --> HW[Hardware]
  ACQ --> RAW[Raw data - ISMRMRD, twix, P-file]
  RAW --> REC[Reconstruction]
  REC --> IMG[Images - DICOM, NIfTI, BIDS]
  IMG --> AN[Analysis - structural, fMRI, dMRI, segmentation]
  REC --> Q[Quantitative MRI and MR spectroscopy]
  AN --> APP[Interpretation and applications]
  Q --> APP
```

## What's inside

The navigator ([`SKILL.md`](skills/mri-research/SKILL.md)) holds a core MR mental
model and routes each question to one of **eleven** reference files — click any
to read it:

| Stage | Reference | Covers |
|---|---|---|
| [Foundations](skills/mri-research/references/foundations.md) | [`foundations.md`](skills/mri-research/references/foundations.md) | MR physics / k-space and where to learn — Berkeley EE225E, Stanford EE369B/C, Hornak, MRIquestions, ISMRM, and the canonical handbooks/textbooks |
| [Acquisition](skills/mri-research/references/sequences-and-trajectories.md) | [`sequences-and-trajectories.md`](skills/mri-research/references/sequences-and-trajectories.md) | Pulse-sequence programming (Pulseq/PyPulseq, vendor SDKs), trajectory design, RF pulse design, SMS/multiband, field mapping, off-resonance, simulation (KomaMRI) |
| [Hardware](skills/mri-research/references/hardware.md) | [`hardware.md`](skills/mri-research/references/hardware.md) | Low-field, open-source consoles (OSI², MaRCoS, OCRA), coils, gradients, MRI safety |
| [Reconstruction](skills/mri-research/references/recon-methods.md) | [`recon-methods.md`](skills/mri-research/references/recon-methods.md) | Landmark-paper reading list: parallel imaging, compressed sensing, low-rank, deep learning, diffusion/score-based, MR fingerprinting, GRASP, denoising, metrics |
| [Recon tools](skills/mri-research/references/tools.md) | [`tools.md`](skills/mri-research/references/tools.md) | BART, SigPy, MIRT.jl, MRIReco.jl, torchkbnufft, gpuNUFFT, mri-nufft, DIRECT, fastMRI, Gadgetron |
| [Data](skills/mri-research/references/data-and-formats.md) | [`data-and-formats.md`](skills/mri-research/references/data-and-formats.md) | ISMRMRD & vendor raw (twix/P-file/Philips), DICOM/NIfTI/BIDS, and open datasets |
| [Analysis](skills/mri-research/references/analysis-processing.md) | [`analysis-processing.md`](skills/mri-research/references/analysis-processing.md) | Structural, functional, diffusion MRI; segmentation & registration; cardiac/body/MSK; radiomics — FreeSurfer, FSL, SPM, ANTs, fMRIPrep, MRtrix3, nnU-Net, MONAI |
| [Quantitative](skills/mri-research/references/quantitative-and-spectroscopy.md) | [`quantitative-and-spectroscopy.md`](skills/mri-research/references/quantitative-and-spectroscopy.md) | Relaxometry, QSM, perfusion/ASL, MT, and MR spectroscopy (LCModel, Osprey, FSL-MRS) |
| [Literature](skills/mri-research/references/literature-access.md) | [`literature-access.md`](skills/mri-research/references/literature-access.md) | APIs, API keys, and paper-search MCP servers (arXiv, PubMed, Semantic Scholar, OpenAlex, Crossref) |
| [Publishing](skills/mri-research/references/publishing.md) | [`publishing.md`](skills/mri-research/references/publishing.md) | MR journals + author guidelines, LaTeX templates, reporting/reproducibility standards, abstracts, preprints |
| [Interpretation](skills/mri-research/references/radiology-primer.md) | [`radiology-primer.md`](skills/mri-research/references/radiology-primer.md) | How MR contrast reads (T1/T2/FLAIR/DWI) — background orientation only |

## Example prompts

- *"I have 8-channel knee k-space undersampled 4×. Walk me through a PI+CS reconstruction with BART."*
- *"What's the canonical paper for ESPIRiT, and how does it differ from SENSE and GRAPPA?"*
- *"I was handed a `meas.dat` file — what is it and how do I reconstruct it in Python?"*
- *"Design a golden-angle radial gradient-echo sequence in PyPulseq and simulate it first."*
- *"Preprocess this task-fMRI dataset and run a first-level GLM — what pipeline should I use?"*
- *"Which open dataset should I benchmark a cardiac cine reconstruction on, and what are the access terms?"*
- *"Summarize the state of diffusion-model MRI reconstruction and point me to codebases."*

## Design principles

- **Point, don't vendor.** Link and summarize; never bundle datasets or copyrighted text.
- **Primary sources first.** Cite the original paper/repo; use awesome-lists as living indexes.
- **Decide, don't just enumerate.** Reference files help you choose the right method/tool.
- **Verify load-bearing links.** Links rot; confirm a link before acting on it.

## Scope & disclaimers

- **Image reading is orientation, not diagnosis.** The reading primer helps
  follow research conversations about contrast; it is not clinical or diagnostic
  advice. Interpretation of real scans belongs to a qualified radiologist.
- **Respect dataset licenses.** Many datasets (fastMRI, HCP, UK Biobank, ADNI,
  OASIS, BraTS) require registration or a data-use agreement; this never helps
  circumvent an access gate.
- **Links can rot.** Every link was verified at release, but repositories move
  and course pages change.

## Contributing

Issues and PRs are welcome — see [`CONTRIBUTING.md`](CONTRIBUTING.md). The one
firm rule: preserve the pointer-not-dump philosophy and verify every link and
citation you add.

## Citing

If this helps your research or tooling, please cite it via the
[`CITATION.cff`](CITATION.cff) metadata (GitHub's "Cite this repository" button
formats it for you).

## Acknowledgements

Built **on top of, and in credit to,** the open MRI community — among them the
Lustig group (UC Berkeley) and the Pauly/Nishimura lineage (Stanford); the BART,
SigPy, ISMRMRD, Gadgetron, and Pulseq ecosystems; the FreeSurfer/FSL/SPM/AFNI/
ANTs and nipreps analysis communities; the fastMRI, mridata.org, HCP, OpenNeuro,
and other dataset efforts; the [ISMRM](https://www.ismrm.org); and the
maintainers of the community awesome-lists. All primary work belongs to its
respective authors. Distribution uses the open [`skills`](https://github.com/vercel-labs/skills) CLI.

## License

Released under the [MIT License](LICENSE). External resources this hub links to
(papers, datasets, software) are governed by their own licenses and terms.
