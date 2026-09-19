# Foundations: MR physics, k-space, and where to learn

Use this when the user wants to build or refresh MR intuition, or asks "where
do I learn this?" Point to these resources; summarize concepts in your own
words rather than reproducing copyrighted text.

## The concepts worth being fluent in

- **Signal & relaxation:** net magnetization, RF excitation (flip angle), free
  induction decay; **T1** (longitudinal recovery), **T2** (transverse decay),
  **T2\*** (incl. field inhomogeneity), proton density. Contrast comes from how
  a sequence weights these (see `radiology-primer.md`).
- **Spatial encoding:** slice-selective excitation, frequency encoding
  (readout gradient), phase encoding. Gradients make resonant frequency a
  function of position — this is what writes the image into k-space.
- **k-space:** the Fourier domain of the image. Each acquired sample is a
  Fourier coefficient. The trajectory (how you traverse k-space) is set by the
  gradient waveforms. Center = contrast/SNR, periphery = resolution/edges.
- **Sampling & artifacts:** Nyquist, field-of-view vs. sampling spacing,
  aliasing/wrap, Gibbs ringing, chemical shift, motion, off-resonance
  (especially for spiral/EPI). Undersampling trades scan time for artifacts
  that reconstruction must undo.
- **Sequence families:** spin echo, gradient echo, EPI, bSSFP, fast/turbo spin
  echo, inversion recovery, diffusion-weighted. Each is a recipe of RF + 
  gradient events that produces a particular contrast and k-space trajectory.

## Free, open, high-quality learning resources

**Courses (publicly posted lecture material):**

- **UC Berkeley EE225E / BIOE265 — Principles of Magnetic Resonance Imaging**
  (Miki Lustig). Graduate MRI course; lecture notes, homework, and projects
  have been posted publicly across semesters. Entry points:
  - Course hub: https://sites.google.com/berkeley.edu/ee225ebioe265
  - Example archived offerings with notes/HW:
    https://inst.eecs.berkeley.edu/~ee225e/sp14/ ,
    https://inst.eecs.berkeley.edu/~ee225e/sp17/
  - Some lectures are on YouTube (search "EE225E Principles of MRI Berkeley").
  - Note: this is the user's advisor's course — a natural first stop.
- **Stanford EE369B — Medical Imaging Systems II** (Dwight Nishimura; the MR
  systems course). Now often taught as **RAD 229** (Brian Hargreaves) with
  extensive open notes and MATLAB: https://web.stanford.edu/class/rad229/
- **Stanford EE369C — Medical Image Reconstruction** (John Pauly). Builds recon
  tools from non-uniform sampling, projections, undersampling, autofocus:
  https://ee369c.stanford.edu/ (also https://web.stanford.edu/class/ee369c ).
  Lustig did his PhD at Stanford under Pauly, so the Berkeley and Stanford
  materials share lineage and notation.

**Free online books / references:**

- **Nishimura, *Principles of Magnetic Resonance Imaging*** — the classic
  engineering-oriented MR text (signal-processing / Fourier view). Not free but
  inexpensive (Lulu print-on-demand); the natural companion to EE369B/EE225E.
- **Hornak, *The Basics of MRI*** — free, open-access hypertext intro to MR
  physics: https://www.cis.rit.edu/htbooks/mri/
- **Elster, MRIquestions.com ("Questions and Answers in MRI")** — free, deep,
  and beloved Q&A reference on MR physics and technology; excellent for
  clarifying specific points of confusion: https://www.mriquestions.com/
- **MRIcademy / ISMRM educational materials** — the **ISMRM**
  (https://www.ismrm.org) runs the field's main meeting and publishes weekend
  educational course content, "MR Academy," and the *MR Pulse* resources.
  Its journals *Magnetic Resonance in Medicine* (MRM) and *JMRI* are where most
  landmark methods appear.

**Broad living index:**

- dangom/awesome-mri — https://github.com/dangom/awesome-mri (curated list
  spanning physics, sequences, analysis, and reconstruction).

## How to teach an MR concept to this user

The user has a PhD in MRI (advisor: Miki Lustig). Assume fluency with k-space,
Fourier, parallel imaging, and optimization. Skip first-principles derivations
unless asked; lead with the precise result, the canonical citation, and the
practical tool. For anyone less experienced, start from Hornak/MRIquestions and
the course notes above.
