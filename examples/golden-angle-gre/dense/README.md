# Dense-phantom correction and validation

This experiment replaces the inadequate 8 mm in-plane point grid in the original
simulation. It keeps the exported 128-spoke GRE sequence, 200 dummy TRs, 33 slice
positions and the established KomaMRI Bloch engine. It evaluates 2 mm, 1 mm and 0.5 mm
in-plane grids with 5 us RF integration steps. Spin densities receive physical
quadrature weights (dx*dy*dz; trapezoidal endpoints in z), so signal amplitudes
can be compared directly across grid refinements.

## Success criteria

1. Recognizable continuous head/brain anatomy on visual inspection, without
   interpolation or smoothing in the display.
2. An off-centre analytic point test with relative error <0.01%, and a
   resolution-matched independent image-recovery test with error <1%.
3. A stable iterative solution (<0.1% image change with extra iterations).
4. A refinement comparison: <5% magnitude-image change between the final two grids. The 2 mm → 1 mm comparison failed (10.1%),
   prompting the 0.5 mm refinement.
   This is a limited in-plane refinement criterion, not proof of full spatial
   convergence; through-slice and finer-grid checks remain separate.

## Reconstruction

SigPy NUFFT, a Fourier-disk constraint (radius 30 on a 64 grid), and L2-regularized
conjugate gradients. The disk restricts the reconstruction to a slightly reduced
radial bandwidth, giving about 3.67 mm nominal resolution; this is an explicit
reconstruction assumption, not a cosmetic image filter. Lambda=0.01 is a
prototype choice, not an optimized parameter. Display interpolation is nearest.
KomaMRI already compensates ADC phase, and SigPy uses (ky,kx)*FOV coordinates.

The old sharp Shepp–Logan test had substantial energy outside this disk. The new
test reports the original separately, projects a reference into the stated
bandwidth, and tests recovery of that reference. It does not claim recovery of
unmeasured sharp detail. The analytic point test checks phase/axis conventions
independently of the image generator.

## Reproduce

From this example directory after setup in the parent README:

```
PYTHON_JULIACALL_HANDLE_SIGNALS=yes JULIA_NUM_THREADS=2 .venv/bin/python dense/simulate_metal.py
.venv/bin/python dense/validate_reconstruction.py
.venv/bin/python dense/reconstruct_dense.py
```

These scripts read `../golden_angle_radial_gre.seq` and `../trajectory.npz`.
They use KomaMRI and SigPy; no custom Bloch simulator or reconstruction solver.

The phantom-density image is a spatial reference, not GRE-contrast ground truth.
The Fourier model omits time-varying magnetization and off-resonance evolution.
This is a noiseless, single-channel simulation, not scanner validation.

## Backend verification

The official `komamripy.load_metal()` installed and enabled KomaMRI's Metal
backend. At 2 mm, single-precision Metal and double-precision CPU signals
agreed to 0.00954% relative norm. The 1 mm CPU job was then deliberately
interrupted because the verified GPU run had completed. Final spatial
comparisons use the same Metal backend/precision at all densities. The CPU
script and 2 mm reference are retained for reproducibility.

## Final results

- 2 mm → 1 mm magnitude-image change: **10.10%**, failed the 5% threshold.
- 1 mm → native 0.5 mm: **5.48%**, still failed. These subsampled maps also
  differ in anatomical sampling; they are not identical continuous objects.
- Native 0.5 mm center samples → four samples per native voxel (0.25 mm
  quadrature spacing): **1.60% magnitude-image change**, passes the scoped
  quadrature criterion. This assumes constant tissue parameters inside each
  native voxel; it adds no anatomical information.
- Final signal residual: **0.777%**; extra iterations change the image only
  at numerical precision. Independent resolution-matched recovery error: **0.0137%**.

The final result uses 13,723,248 quadrature points, simulated in four batches
of 3,430,812 spins and averaged with equal volume weights. Each batch executes
the same full exported sequence in KomaMRI. Run `simulate_subvoxel.py` after
`simulate_metal.py`, then `reconstruct_dense.py`. All reports retain failed
intermediate checks. This is a useful prototype image, not proof of convergence
in z, RF integration at this density, or all aspects of the physical model.

Phantom provenance: KomaMRI `brain_phantom2D`, based on BrainWeb.
https://brainweb.bic.mni.mcgill.ca/brainweb/
Cocosco et al. (1997); Collins et al. (1998); Aubert-Broche et al. (2006).
