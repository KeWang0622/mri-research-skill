# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.6.0] — 2026-09-22

More tools across sequence design and hardware/RF, a multi-agent red-team
improvement pass, and stronger CI + branch protection.

### Added
- **Sequence design:** gradient/trajectory optimization (GrOpt, Lustig
  minTimeGradient, safe_pns_prediction), GIRF (MRI-gradient/GIRF, GIRFReco.jl),
  Pulseq ecosystem (TOPPE for GE, pulseq-CEST, MR-Physics-with-Pulseq), more
  simulators (JEMRIS, MRiLab, sycomore, EPG-X, MRzero-Core), and RF design
  (pulpy, Spectral-Spatial-RF-Pulse-Design, Multiband-RF, kpTx).
- **Hardware / RF:** coil design (CoilGen, pyCoilGen), EM/SAR (MARIE, mariepy,
  CoSimPy, scikit-rf), B0 shimming (Shimming Toolbox), the MaRCoS ecosystem
  (marcos_client/server, marga, ocra-pulseq), GPA-FHDO, MRI4ALL, and OSI² ONE
  (with the correction that OSI² code lives on GitLab).
- **Reconstruction:** CG-SENSE and partial-Fourier/homodyne. **Quantitative:**
  fat–water (Dixon / IDEAL / PDFF / R2*) and CEST.
- **CI:** a committed `validate_repo.py` (frontmatter + registry↔folder
  consistency) and a "skills CLI detects all skills" job.

### Changed / Fixed (multi-agent red-team pass)
- `mri-reconstruction`: `bart_recon.sh` now states its assumptions (Cartesian,
  coils on dim 3, ACS required), adds an explicit **trajectory path** for
  non-Cartesian data instead of silently FFT-ing it, and the docs no longer
  overclaim ("just works" → scoped to Cartesian; non-Cartesian needs a
  trajectory). Named the real `.cfl` conversion mechanisms.
- Rescoped the `mri-research` hub description to orientation/routing so it no
  longer over-triggers and collides with every expert.
- Foundations: disambiguated ISMRM "MR Academy" (dropped the unrelated
  "MRIcademy" brand). Aligned all version numbers.

### Governance
- Branch protection on `main`: PRs must pass the CI status checks before merge.

## [0.5.1] — 2026-09-19

Industry-standard hardening (no skill-content changes).

### Added
- Community health: `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1),
  `SECURITY.md`, issue templates, and a pull-request template.
- CI (`.github/workflows/validate.yml`): validates `skills.sh.json` and every
  SKILL.md's frontmatter, runs ShellCheck on the helper script, and link-checks
  all Markdown (tolerant of publisher bot-blocks) on each change and weekly.
- `.editorconfig`.

### Fixed
- Repointed the README stars-badge link to the repo home (the `/stargazers` path
  returned 404 to link checkers).

### Verified
- Full link sweep across every file: 172 URLs return 200; the remainder are
  publisher pages that bot-block (403/429) but load in a browser.

## [0.5.0] — 2026-09-19

Added an end-to-end **research-workflow** agent that shepherds a project from
idea to a published paper.

### Added
- `skills/mri-research-workflow/` — orchestrator/assistant for the full research
  lifecycle (literature → hypothesis → experiment design → running experiments →
  analysis → figures/tables → manuscript → submission/rebuttal). Venue-aware for
  **CVPR / MICCAI / NeurIPS / MRM**, with template and reproducibility pointers
  (cvpr-org/author-kit, Springer LNCS, MRM LaTeX class, Papers with Code,
  CLAIM/COBIDAS). Hands off to the expert agents.

### Changed
- `skills.sh.json` adds a "Research workflow" group; README and the hub SKILL.md
  list the new agent. Version 0.5.0.

## [0.4.0] — 2026-09-19

Turned the repo into a multi-agent MRI **team**: five specialized, installable
expert skills alongside the generalist hub, with the reconstruction agent made
**actionable** (it runs BART/SigPy).

### Added
- `skills/mri-reconstruction/` — actionable reconstruction agent (ESPIRiT +
  PI/CS via BART/SigPy) including a runnable `scripts/bart_recon.sh`.
- `skills/diffusion-mri/` — diffusion MRI (DTI/DKI/NODDI, topup/eddy, CSD,
  tractography; MRtrix3, DIPY, FSL, AMICO, TractSeg, QSIPrep).
- `skills/pulse-sequence-design/` — Pulseq/PyPulseq, KomaMRI, RF/SMS design, and
  Siemens (IDEA/ICE) / GE (EPIC/Orchestra) / Philips (Paradise) sequence dev.
- `skills/deep-learning-recon/` — unrolled / self-supervised / diffusion recon,
  DIRECT/fastMRI/mridc, evaluation & hallucination caveats.
- `skills/mri-hardware/` — low-field, open-source consoles, coils, MR safety.
- `skills.sh.json` groups the hub and the expert team.

### Changed
- `mri-research` hub gains an "expert team" section pointing to the siblings
  (version 0.4.0). README documents the team and per-skill install
  (`--skill <name>` / `--all`).

## [0.3.0] — 2026-09-19

Deepened coverage (review-driven) and added a publishing reference.

### Added
- `references/publishing.md` — MR journals + author guidelines (MRM, JMRI, NMR in
  Biomedicine, MAGMA, IEEE TMI, Medical Image Analysis, NeuroImage, Imaging
  Neuroscience, Radiology), LaTeX templates/classes (MRM class, IEEEtran,
  elsarticle, Springer, Overleaf, arXiv), reporting/reproducibility standards
  (COBIDAS, CLAIM, TRIPOD+AI, ISMRM RRSG), and abstract submission.
- `sequences-and-trajectories.md` — acquisition-side acceleration & correction:
  SMS/multiband (Moeller 2010, Setsompop 2012, CMRR), B0 field mapping &
  distortion correction (FSL topup/FUGUE), B1 mapping, off-resonance correction,
  prospective motion.
- `recon-methods.md` — GRASP/XD-GRASP (motion-resolved), subspace/low-rank
  model-based qMRI, a denoising section (NORDIC, MP-PCA, Patch2Self), and an
  evaluation & image-quality-metrics section (SSIM/PSNR/…, DL-hallucination
  caveat, retired-leaderboard note).
- `analysis-processing.md` — quality control & motion (MRIQC, MCFLIRT), and a
  cardiac/body/MSK + radiomics section (pyradiomics; ACDC/M&Ms benchmarks).
- `data-and-formats.md` — ACDC and M&Ms cardiac datasets.
- `hardware.md` — a dedicated, non-clinical MRI safety section (ACR,
  MRIsafety.com, ISMRM).
- README Mermaid pipeline diagram.

### Changed
- `SKILL.md` routing and triggers extended (publishing, safety); version 0.3.0.

## [0.2.0] — 2026-09-19

Broadened from a reconstruction-focused reference into a **general MRI** research
hub, and switched distribution to the open `skills` CLI (`npx skills add`).

### Added
- `references/analysis-processing.md` — image analysis & processing: structural,
  functional, and diffusion MRI; segmentation and registration; DICOM/NIfTI/BIDS
  handling. Tools include FreeSurfer, FSL, SPM, AFNI, ANTs, fMRIPrep, nilearn,
  MRtrix3, DIPY, nnU-Net, TotalSegmentator, MONAI, Nipype, dcm2niix, nibabel.
- `references/quantitative-and-spectroscopy.md` — quantitative MRI (relaxometry,
  QSM, perfusion/ASL, MT) and MR spectroscopy (LCModel, Osprey, FSL-MRS, Gannet,
  qMRLab, SEPIA).
- `references/data-and-formats.md` — image-level formats (DICOM, NIfTI, BIDS) and
  image-level datasets (HCP, OpenNeuro, UK Biobank, ADNI, OASIS, IXI, BraTS) with
  access-term notes.
- `references/foundations.md` — canonical textbooks/handbooks (McRobbie,
  Westbrook, Bernstein *Handbook of MRI Pulse Sequences*, Haacke).
- `skills.sh.json` registry metadata for the `skills` ecosystem.

### Changed
- `SKILL.md` reframed around the full MRI pipeline (physics → acquisition →
  reconstruction → analysis → quantification) with an expanded routing table.
- Repository restructured to the `skills` layout (`skills/mri-research/`) so it
  installs with `npx skills add KeWang0622/mri-research-skill`.
- README rewritten: MRI-first framing, `npx skills` install, working badges.

## [0.1.0] — 2026-09-19

Initial public release.

### Added
- `SKILL.md` navigator: core MR mental model, ground rules (link rot, dataset
  licenses, non-diagnostic scope, no copyrighted text), and a question →
  reference routing table.
- `references/foundations.md` — MR physics / k-space and where to learn
  (UC Berkeley EE225E, Stanford EE369B/C, Hornak, MRIquestions, ISMRM).
- `references/recon-methods.md` — landmark-paper reading list spanning parallel
  imaging (SENSE, GRAPPA, ESPIRiT, SPIRiT, NLINV), compressed sensing, low-rank
  and dynamic (L+S, k-t, structured low-rank), deep learning (VarNet, MoDL,
  E2E-VarNet, SSDU, AUTOMAP), diffusion / score-based recon, and MR
  fingerprinting; plus a "which method for which task" guide.
- `references/tools.md` — toolbox decision guide and usage patterns for BART,
  SigPy, MIRT.jl, MRIReco.jl, torchkbnufft, gpuNUFFT, mri-nufft, pygrappa,
  DIRECT, fastMRI, DeepInPy, TensorFlow MRI, and Gadgetron.
- `references/data-and-formats.md` — ISMRMRD and vendor raw formats (Siemens
  twix, GE P-file, Philips raw) with converters, plus open datasets (fastMRI,
  mridata.org, OCMR, SKM-TEA, Calgary-Campinas, CMRxRecon, M4Raw).
- `references/sequences-and-trajectories.md` — pulse-sequence programming
  (Pulseq/PyPulseq, vendor SDKs), trajectory design, and simulation (KomaMRI).
- `references/hardware.md` — MRI hardware and the open-hardware community
  (OSI², MaRCoS, OCRA, low-field, coils, gradients, safety).
- `references/literature-access.md` — literature/data APIs, API-key handling,
  and paper-search MCP servers.
- `references/radiology-primer.md` — MR image-contrast orientation (T1/T2/
  FLAIR/DWI), scoped strictly as non-diagnostic background.
- Project scaffolding: `README.md`, `LICENSE` (MIT), `CITATION.cff`,
  `CONTRIBUTING.md`, `.gitignore`.

[0.1.0]: https://github.com/KeWang0622/mri-research-skill/releases/tag/v0.1.0
