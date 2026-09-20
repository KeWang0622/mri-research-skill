# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
