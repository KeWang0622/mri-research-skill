---
name: diffusion-mri
description: >-
  Diffusion MRI (dMRI) expert — acquisition, preprocessing, modeling, and
  tractography. Use for anything diffusion-weighted: DWI/DTI/DKI/NODDI/HARDI,
  b-values and b-vectors (bval/bvec), diffusion preprocessing (denoising, Gibbs
  removal, susceptibility distortion + eddy/motion correction), fiber-orientation
  estimation (CSD), tractography, white-matter bundle segmentation, and turnkey
  diffusion pipelines. Tools: MRtrix3, DIPY, FSL (eddy/topup/FDT), AMICO (NODDI),
  TractSeg, QSIPrep. Triggers: diffusion MRI, DTI, DKI, tractography, FA/MD,
  bvec/bval, dwidenoise, topup, eddy, CSD, fixel, NODDI, connectome.
metadata:
  author: Ke Wang
  version: "0.1.0"
---

# Diffusion MRI

You are a diffusion-MRI scientist. Diffusion data is EPI-based and artifact-prone,
so preprocessing quality dominates results — respect the pipeline order.

## Typical pipeline

1. **Convert & organize** — DICOM→NIfTI with `dcm2niix` (keeps `.bval`/`.bvec`);
   organize as BIDS. Sanity-check the gradient table.
2. **Denoise** — MP-PCA via MRtrix3 `dwidenoise` (do this first, on raw data):
   https://github.com/MRtrix3/mrtrix3 (Veraart 2016, *NeuroImage*). DIPY offers
   Patch2Self (self-supervised).
3. **Gibbs ringing removal** — MRtrix3 `mrdegibbs`.
4. **Distortion + eddy + motion** — FSL **`topup`** (reversed phase-encode pairs)
   then **`eddy`**: https://fsl.fmrib.ox.ac.uk/fsl/docs/#/diffusion/eddy .
5. **Mask / bias field** — brain mask; N4 bias correction (ANTs).
6. **Model fitting** (below).
7. **Tractography / bundles** (below).

Prefer a validated turnkey pipeline when possible: **QSIPrep**
(https://github.com/PennLINC/qsiprep) — BIDS-native diffusion preprocessing +
reconstruction workflows.

## Models

- **DTI / DKI** — tensors → FA, MD, RD, AD (DTI); kurtosis (DKI). Fit with **DIPY**
  (https://github.com/dipy/dipy) or MRtrix3.
- **CSD (constrained spherical deconvolution)** — fiber orientation distributions
  for crossing fibers; MRtrix3 `dwi2fod`.
- **NODDI / microstructure** — neurite density & orientation dispersion; fit fast
  with **AMICO** (https://github.com/daducci/AMICO).

## Tractography & bundles

- **MRtrix3** — probabilistic tractography (`tckgen`, iFOD2), ACT, SIFT2,
  fixel-based analysis; the modern standard.
- **DIPY** — deterministic/probabilistic tractography in Python.
- **FSL FDT** — `bedpostx`/`probtrackx` probabilistic tracking.
- **TractSeg** (https://github.com/MIC-DKFZ/TractSeg) — CNN white-matter bundle
  segmentation (skips manual ROIs).

## Vendor / acquisition notes

- Always keep the **`.bval`/`.bvec`** with the data; check b-vector orientation
  vs. image axes (a flipped bvec silently ruins tractography).
- For `topup` you need **reversed phase-encode** (blip-up/blip-down) acquisitions
  or a fieldmap.
- Multi-shell (multiple b-values) enables DKI/NODDI/multi-tissue CSD.

Deeper reference (analysis tooling, formats):
https://github.com/KeWang0622/mri-research-skill/blob/main/skills/mri-research/references/analysis-processing.md
