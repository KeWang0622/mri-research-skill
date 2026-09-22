#!/usr/bin/env bash
#
# Parallel-imaging + compressed-sensing MRI reconstruction with BART.
#
# Usage:
#   bart_recon.sh <kspace_cfl> <output_cfl> [l1_reg] [traj_cfl]
#
# Assumptions — VERIFY these before trusting the output; the script warns but
# cannot fully check them:
#   * <kspace_cfl> is a BART .cfl/.hdr file in BART's dimension order, i.e.
#     coils on dimension 3:  [X  Y  Z  COILS  ...].  A .cfl written with a
#     different axis order (e.g. from a NumPy array) will reconstruct to garbage.
#   * ESPIRiT needs a fully-sampled calibration region (ACS) near the center of
#     k-space (or fully-sampled data). Prospectively uniform undersampling with
#     NO ACS gives wrong coil maps — and no error.
#   * With no trajectory (4th arg) the data is treated as CARTESIAN. That is the
#     right path for Cartesian GRE/TSE *and for EPI*: EPI traverses k-space in a
#     zig-zag but its samples lie on a Cartesian grid, so it needs ramp-sampling
#     regridding and Nyquist-ghost / phase correction UPSTREAM of this script,
#     not a NUFFT. Pass a trajectory .cfl only for genuinely non-Cartesian
#     sampling: radial, spiral, cones, rosette, PROPELLER. This script refuses
#     to guess.
#
# Requires BART on PATH. BART's active home moved to Codeberg in 2026:
#   https://codeberg.org/mrirecon/bart   (docs: https://mrirecon.codeberg.page/)
# The github.com/mrirecon/bart repository is archived and no longer updated.
set -euo pipefail

KSP="${1:?usage: bart_recon.sh <kspace_cfl> <output_cfl> [l1_reg] [traj_cfl]}"
OUT="${2:?usage: bart_recon.sh <kspace_cfl> <output_cfl> [l1_reg] [traj_cfl]}"
REG="${3:-0.01}"   # L1-wavelet regularization strength
TRAJ="${4:-}"      # optional BART trajectory .cfl (required for non-Cartesian)

command -v bart >/dev/null 2>&1 || {
  echo "ERROR: BART not found on PATH. Install: https://codeberg.org/mrirecon/bart" >&2; exit 1; }
[ -f "${KSP}.cfl" ] && [ -f "${KSP}.hdr" ] || {
  echo "ERROR: need BART files ${KSP}.cfl and ${KSP}.hdr. Convert vendor/ISMRMRD" >&2
  echo "       raw to .cfl first (see SKILL.md)." >&2; exit 1; }

# Refuse to clobber existing intermediates/outputs the user may care about.
for f in "$OUT" "${OUT}_sens"; do
  if [ -f "${f}.cfl" ]; then
    echo "ERROR: ${f}.cfl already exists — refusing to overwrite. Choose another" >&2
    echo "       output name or remove it first." >&2; exit 1
  fi
done

# Intermediates are scratch; clean them up on exit so a rerun is reproducible.
TMPBASE="$(mktemp -u "${TMPDIR:-/tmp}/bart_recon_XXXXXX")"
cleanup() { rm -f "${TMPBASE}"*.cfl "${TMPBASE}"*.hdr; }
trap cleanup EXIT

echo ">> k-space dimensions (expect coils on dim 3:  X Y Z COILS ...):"
bart show -m "$KSP"
echo ">> REMINDER: ESPIRiT assumes a fully-sampled calibration region (ACS) near"
echo "   k-space center. If undersampling removed the ACS, coil maps are wrong."

# -m1 is essential: `bart ecalib` computes TWO ESPIRiT map sets by default, which
# makes `pics` emit a soft-SENSE result with a size-2 MAPS dimension rather than
# a single image. -r caps the auto-extracted calibration region (24^3 is BART's
# default; lower it if your ACS is smaller than that).
if [ -n "$TRAJ" ]; then
  [ -f "${TRAJ}.cfl" ] && [ -f "${TRAJ}.hdr" ] || {
    echo "ERROR: need trajectory files ${TRAJ}.cfl and ${TRAJ}.hdr." >&2; exit 1; }
  echo ">> Non-Cartesian path (trajectory supplied): gridded calibration + PICS -t."
  echo "   This is a sensible default; verify it suits your trajectory/data."
  # Use the INVERSE nufft, not the adjoint: the adjoint leaves the sampling
  # density in the data (for radial, density ~ 1/|k|), so FFT-ing it back to a
  # grid hands ESPIRiT systematically mis-weighted k-space and biases the maps.
  # If BART cannot infer the image size here, pass -d X:Y:Z explicitly.
  bart nufft -i "$TRAJ" "$KSP" "${TMPBASE}_cimg"
  bart fft -u 7 "${TMPBASE}_cimg" "${TMPBASE}_gridksp"
  bart ecalib -m1 -r 24 "${TMPBASE}_gridksp" "${OUT}_sens"
  bart pics -l1 -r "$REG" -t "$TRAJ" "$KSP" "${OUT}_sens" "$OUT"
else
  echo ">> Cartesian path (no trajectory): ESPIRiT + L1-wavelet PICS."
  bart ecalib -m1 -r 24 "$KSP" "${OUT}_sens"
  bart pics -l1 -r "$REG" "$KSP" "${OUT}_sens" "$OUT"
fi

echo ">> Done. Reconstructed image: ${OUT}.cfl/.hdr (coil maps: ${OUT}_sens)."
echo ">> Output dimensions (dim 3 = 1 coil, dim 4 = 1 map if this went right):"
bart show -m "$OUT"
echo "   Tune -r (arg 3, default ${REG}): raise if aliasing remains, lower if"
echo "   the image looks over-smoothed."
