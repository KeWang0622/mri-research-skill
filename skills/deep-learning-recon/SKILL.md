---
name: deep-learning-recon
description: >-
  Deep-learning MRI reconstruction expert. Use for training or applying neural
  networks to reconstruct undersampled MRI — unrolled / variational networks
  (VarNet, MoDL, End-to-End VarNet, deep cascade), self-supervised training
  without fully-sampled data (SSDU), diffusion / score-based reconstruction, and
  the frameworks and datasets to do it. Tools: DIRECT, fastMRI, mridc,
  torchkbnufft; datasets fastMRI / mridata. Triggers: deep learning
  reconstruction, unrolled network, variational network, MoDL, end-to-end
  VarNet, data consistency, self-supervised MRI reconstruction, diffusion model
  reconstruction, score-based, fastMRI, physics-guided network.
metadata:
  author: Ke Wang
  version: "0.1.0"
---

# Deep-Learning MRI Reconstruction

You are a DL-recon researcher. The dominant, robust paradigm is the **unrolled
network**: unroll N iterations of an iterative solver, learn the
regularizer/updates end-to-end, and keep the measured **data-consistency** step.
Always anchor to data consistency — it's what guards against hallucinated
structure.

## Method families (with citations)

- **Variational Network (VN)** — Hammernik et al., *MRM* 2018;79(6):3055–3071.
  Code: https://github.com/VLOGroup/mri-variationalnetwork
- **MoDL** — CNN prior + CG data consistency, weight-shared. Aggarwal et al.,
  *IEEE TMI* 2019. Code: https://github.com/hkaggarwal/modl
- **End-to-End VarNet** — learns coil sensitivities too; strong fastMRI baseline
  (Sriram et al., MICCAI 2020) — in the fastMRI repo.
- **SSDU (self-supervised, no fully-sampled data)** — split acquired k-space into
  DC and loss sets. Yaman et al., *MRM* 2020. Code:
  https://github.com/byaman14/SSDU
- **Diffusion / score-based** — learned generative prior + measurement
  consistency; sampling-pattern-agnostic, inference-heavy. Chung & Ye, *MedIA*
  2022 (https://github.com/hyungjin-chung/score-MRI); Jalal et al., NeurIPS 2021
  (https://github.com/utcsilab/csgm-mri-langevin).
- **AUTOMAP** — end-to-end domain-transform learning (Zhu et al., *Nature* 2018);
  instructive but memory-heavy.

## Frameworks & building blocks

- **DIRECT** — https://github.com/NKI-AI/direct — many baselines + training loops.
- **fastMRI** — https://github.com/facebookresearch/fastMRI — reference models
  (U-Net, VarNet, E2E-VarNet), transforms, and challenge-matched evaluation.
- **mridc** — https://github.com/wdika/mridc — data-consistency-focused toolbox.
- **torchkbnufft** — https://github.com/mmuckley/torchkbnufft — differentiable
  NUFFT to drop non-Cartesian physics into a network.

## Data

**fastMRI** (knee/brain/prostate/breast) is the benchmark; requires a signed
**data-use agreement** (https://fastmri.med.nyu.edu). Fully-open alternative for
prototyping: mridata.org.

## Training & evaluation

- Report **SSIM, PSNR, NMSE** (and perceptual VIF/LPIPS) — but no single metric
  guarantees diagnostic quality; pair with reader assessment as the fastMRI
  challenges did.
- **Watch for hallucination:** generative/high-acceleration recon can synthesize
  plausible but false structure. Test stability and out-of-distribution
  robustness; prefer data-consistency-anchored architectures.

Deeper reference:
https://github.com/KeWang0622/mri-research-skill/blob/main/skills/mri-research/references/recon-methods.md
