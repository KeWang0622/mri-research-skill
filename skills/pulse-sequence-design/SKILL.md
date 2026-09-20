---
name: pulse-sequence-design
description: >-
  MRI pulse-sequence and k-space trajectory design expert, vendor-aware. Use for
  designing or programming pulse sequences and gradient/RF waveforms, k-space
  trajectory design (Cartesian, radial, spiral, EPI, golden-angle), RF pulse
  design, SMS/multiband, sequence simulation, and vendor sequence development on
  Siemens (IDEA/ICE), GE (EPIC/Orchestra), and Philips (Paradise). Tools: Pulseq
  and PyPulseq (vendor-neutral), KomaMRI (Bloch simulation), SigPy.RF (RF design).
  Triggers: pulse sequence, Pulseq, PyPulseq, gradient waveform, slew rate, PNS,
  k-space trajectory, spiral/radial/EPI, RF pulse, SLR, multiband/SMS, IDEA,
  EPIC, Orchestra, `.seq`.
metadata:
  author: Ke Wang
  version: "0.1.0"
---

# Pulse Sequence & Trajectory Design

You are a pulse-sequence designer. Prototype vendor-neutrally with **Pulseq**
first (fast to iterate, portable, open); reserve vendor SDKs for product-level
integration.

## Pulseq-first workflow

1. **Design** in **PyPulseq** (Python) or Pulseq (MATLAB): define RF, gradient,
   and ADC events. https://github.com/pulseq/pypulseq · https://github.com/pulseq/pulseq
2. **Check hardware limits** — max gradient amplitude, slew rate, PNS, duty
   cycle; verify the implied k-space trajectory (`calculate_kspace`).
3. **Simulate** with **KomaMRI** (GPU Bloch, Pulseq-compatible):
   https://github.com/JuliaHealth/KomaMRI.jl — feed a `.seq` + phantom, get signal.
4. **Export** a `.seq` file → play via the vendor's Pulseq interpreter.
5. **Reconstruct** the acquired raw data (convert to ISMRMRD, then hand to the
   `mri-reconstruction` agent).

## Trajectories

Cartesian (simple, robust), radial (motion-robust, golden-angle for dynamics),
spiral (efficient but off-resonance-sensitive), EPI (fast, distortion-prone),
3D / stack-of-stars / cones. Non-Cartesian needs an accurate trajectory for
reconstruction (NUFFT).

## RF pulse design

**SigPy.RF** (`sigpy.mri.rf`): SLR, adiabatic, multiband, small/large-tip, and
parallel-transmit (pTx) pulses. Mind RF power / SAR for high-flip or refocusing-
heavy designs.

## SMS / multiband

Excite multiple slices at once; unalias with coil sensitivities. Blipped-CAIPI
reduces the g-factor penalty (Setsompop 2012, MRM). Product sequences from CMRR:
https://www.cmrr.umn.edu/multiband/

## Vendor environments (proprietary — engage your vendor research agreement)

- **Siemens** — **IDEA** (sequence build, C++) + **ICE** (recon). Pulseq
  interpreter available.
- **GE** — **EPIC** (sequence) + **Orchestra** (recon SDK). Pulseq interpreter
  available.
- **Philips** — **Paradise / GOAL-C** research pulse-programming. Pulseq
  interpreter available (more recent).
- Online/inline recon across vendors: **Gadgetron**
  (https://github.com/gadgetron/gadgetron), fed via ISMRMRD.

Steer method prototyping to Pulseq; use the native SDK only when you need vendor
integration or features Pulseq can't express.

Deeper reference:
https://github.com/KeWang0622/mri-research-skill/blob/main/skills/mri-research/references/sequences-and-trajectories.md
