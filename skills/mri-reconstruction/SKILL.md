---
name: mri-reconstruction
description: >-
  Actionable MRI image reconstruction — turn raw k-space into an image, and
  actually run it. Use this WHENEVER the user wants to reconstruct MR data or
  says things like "reconstruct this k-space", "run BART on this", "get an image
  from this .cfl / .h5 / twix file", or asks about parallel imaging
  (ESPIRiT/SENSE/GRAPPA), compressed sensing (PICS / L1-wavelet), coil
  sensitivity estimation, coil combination, or non-Cartesian / NUFFT
  reconstruction. This agent prefers to EXECUTE the reconstruction with BART or
  SigPy (not just describe it). Triggers: k-space, coil sensitivities, ESPIRiT,
  PICS, undersampled reconstruction, radial/spiral recon, `.cfl`/`.hdr`,
  ISMRMRD, Siemens twix, GE P-file.
metadata:
  author: Ke Wang
  version: "0.1.0"
---

# MRI Reconstruction (actionable)

You are a reconstruction engineer: given k-space, produce an image — and run the
pipeline, don't just talk about it. Default to **BART** (battle-tested, CLI,
scriptable); use **SigPy** when the user is in Python. Confirm the data before
running, then execute and inspect.

## Workflow

**0. Identify the k-space format** (ask or inspect). BART reads its own `.cfl`;
it does **not** natively ingest NumPy or ISMRMRD, so those need an explicit
write step:
- **BART `.cfl` + `.hdr`** — native; dims must be `[X Y Z COILS ...]` (coils on
  dim 3). Ready to use.
- **Siemens twix `.dat`** — `bart twixread` writes a `.cfl` directly; or read in
  Python with `twixtools`/`pymapVBVD` then write a `.cfl`.
- **NumPy array** — write a `.cfl` with BART's Python helper
  `cfl.writecfl(name, array)` (shipped in BART's `python/` dir; also `bartpy`).
  Make sure coils land on dim 3.
- **ISMRMRD `.h5`** — read with the Python `ismrmrd` package (or Gadgetron),
  assemble the k-space array, then `cfl.writecfl`. Vendor raw → ISMRMRD first
  via `siemens_to_ismrmrd` / `ge_to_ismrmrd` / `philips_to_ismrmrd`.

**1. Estimate coil sensitivities (ESPIRiT):**
```
bart ecalib -r 24 kspace sens        # -r = calibration region size
```

**2. Reconstruct:**
```
# Fully sampled: inverse FFT + coil combine
bart fft -iu 7 kspace img_coils && bart rss 8 img_coils img

# Undersampled — parallel imaging + compressed sensing (the workhorse):
bart pics -l1 -r 0.01 kspace sens img     # l1-wavelet regularized
```
- **Non-Cartesian** (radial/spiral): you also need the trajectory. Use
  `bart pics -t traj kspace sens img` (or `bart nufft` for the adjoint). Get the
  trajectory from the sequence/ISMRMRD, or `bart traj` for nominal.

**3. Inspect:** check image dimensions, scaling, and orientation; look for
residual aliasing (raise `-r`), over-smoothing (lower `-r`), or coil-combination
errors.

## Runnable helper

`scripts/bart_recon.sh <kspace_cfl> <output_cfl> [l1_reg] [traj_cfl]` runs an
ESPIRiT → PI+CS pipeline on a BART `.cfl` k-space file. It **assumes Cartesian
data with coils on dim 3 and a fully-sampled ACS** (calibration region); pass a
**trajectory `.cfl`** as the 4th argument for radial/spiral/EPI. It warns about
these assumptions but can't fully verify them — check the header and adapt the
regularization / calibration size to the data.

## SigPy (Python) alternative

```python
import sigpy as sp, sigpy.mri as mr
maps = mr.app.EspiritCalib(ksp).run()                     # coil maps
img  = mr.app.L1WaveletRecon(ksp, maps, lamda=0.01).run() # PI + CS
# non-Cartesian: build a NUFFT from coords, use mr.app.SenseRecon
```

## Guardrails

- Confirm the acceleration factor and sampling (Cartesian vs non-Cartesian)
  before choosing a method — the wrong forward model gives garbage.
- If BART isn't installed: https://mrirecon.github.io/bart/ (docs) — offer to
  install or fall back to SigPy.
- For method theory and citations, see the hub:
  https://github.com/KeWang0622/mri-research-skill/blob/main/skills/mri-research/references/recon-methods.md
  and tool details at
  https://github.com/KeWang0622/mri-research-skill/blob/main/skills/mri-research/references/tools.md
