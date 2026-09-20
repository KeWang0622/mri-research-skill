# Quantitative MRI (qMRI) & MR spectroscopy (MRS)

Use this when the goal is **parameter maps or metabolite concentrations**, not a
single qualitative image — relaxometry, susceptibility, perfusion, magnetization
transfer, and spectroscopy. These methods pair a specialized acquisition with a
model-fitting step, so they sit between acquisition (`sequences-and-
trajectories.md`) and analysis ([`analysis-processing.md`](analysis-processing.md)). Links verified;
point users to each tool's own docs.

## Quantitative MRI (parameter mapping)

The idea: acquire several images with varying sequence parameters, then fit a
signal model per voxel to recover a physical quantity (T1, T2, T2\*, PD, MT,
susceptibility, perfusion). Reproducible and scanner-comparable, unlike
weighted images.

- **qMRLab** — https://github.com/qMRLab/qMRLab — a broad, multi-method toolbox
  for simulating, fitting, and visualizing many qMRI models (T1/T2 relaxometry,
  MT/ihMT, diffusion, field mapping). The best general starting point for qMRI
  methods and teaching.
- **hMRI toolbox** — https://github.com/hMRI-group/hMRI-toolbox — SPM-based
  multi-parameter mapping (R1, R2\*, PD, MT) for "in-vivo histology"
  (microstructure) studies.
- **Relaxometry basics:** T1 mapping (e.g., variable flip angle, MP2RAGE,
  inversion recovery), T2/T2\* mapping (multi-echo). For **MR fingerprinting**
  — a one-shot route to simultaneous T1/T2 maps — see the fingerprinting entry
  in [`recon-methods.md`](recon-methods.md); its reconstruction and quantification are intertwined.

## Quantitative susceptibility mapping (QSM)

Recovers tissue magnetic susceptibility (iron, calcium, myelin, venous blood)
from gradient-echo phase. A multi-step pipeline (phase unwrapping → background-
field removal → dipole inversion).

- **SEPIA** — https://github.com/kschan0214/sepia — a MATLAB GUI that chains
  established QSM algorithms into a reproducible pipeline; good for
  standardizing a QSM workflow rather than reimplementing each step.

## Perfusion

- **Arterial spin labeling (ASL)** — magnetically labels arterial blood as an
  endogenous tracer to quantify cerebral blood flow. Fit with **BASIL /
  oxford_asl** (part of FSL): https://fsl.fmrib.ox.ac.uk/fsl/docs/#/perfusion/asl
  (Python port **oxasl**: https://github.com/physimals/oxasl).
- **DSC / DCE** — dynamic susceptibility contrast and dynamic contrast-enhanced
  perfusion use gadolinium bolus tracking (note: gadolinium is a contrast agent
  — a clinical/safety consideration, out of scope for method tooling here).

## MR spectroscopy (MRS)

Measures the concentration of metabolites (NAA, creatine, choline, lactate,
GABA, …) from the chemical-shift spectrum rather than forming an image. Common
localization: single-voxel PRESS/STEAM, and edited MEGA-PRESS for GABA.

- **LCModel** — http://www.lcmodel.com/ — the long-standing reference for
  linear-combination metabolite quantification. Closed-source but free to
  download (since 2020); still a common comparison baseline.
- **Osprey** — https://github.com/schorschinho/osprey — modern all-in-one
  open-source MRS processing and quantification (MATLAB); a good default for new
  work.
- **FSL-MRS** — https://github.com/wtclarke/fsl_mrs — Python MRS preprocessing,
  fitting, and quantification (the maintained GitHub mirror; the FMRIB docs host
  had a stale TLS cert at last check).
- **Gannet** — https://github.com/markmikkelsen/Gannet — the standard tool for
  GABA-edited (MEGA-PRESS) MRS analysis.
- **Tarquin** — http://tarquin.sourceforge.net/ — open-source automated 1H-MRS
  quantification (hosted on SourceForge; no maintained GitHub repo).

## Which tool for which task

- *General qMRI modeling / simulation / fitting* → qMRLab; hMRI toolbox for
  SPM-based multi-parameter maps.
- *Susceptibility maps from GRE phase* → SEPIA.
- *Cerebral blood flow from ASL* → BASIL / oxford_asl (or oxasl in Python).
- *Metabolite quantification* → Osprey or FSL-MRS for open pipelines; LCModel as
  the reference baseline; Gannet specifically for GABA-edited data.
