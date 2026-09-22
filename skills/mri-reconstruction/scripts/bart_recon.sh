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
#   * With no trajectory (4th arg) the data is treated as CARTESIAN. For
#     radial / spiral / EPI non-Cartesian data you MUST pass a trajectory .cfl,
#     otherwise the FFT forward model is wrong. This script refuses to guess.
#
# Requires BART on PATH: https://mrirecon.github.io/bart/
set -euo pipefail

KSP="${1:?usage: bart_recon.sh <kspace_cfl> <output_cfl> [l1_reg] [traj_cfl]}"
OUT="${2:?usage: bart_recon.sh <kspace_cfl> <output_cfl> [l1_reg] [traj_cfl]}"
REG="${3:-0.01}"   # L1-wavelet regularization strength
TRAJ="${4:-}"      # optional BART trajectory .cfl (required for non-Cartesian)

command -v bart >/dev/null 2>&1 || {
  echo "ERROR: BART not found on PATH. Install: https://mrirecon.github.io/bart/" >&2; exit 1; }
[ -f "${KSP}.cfl" ] && [ -f "${KSP}.hdr" ] || {
  echo "ERROR: need BART files ${KSP}.cfl and ${KSP}.hdr. Convert vendor/ISMRMRD" >&2
  echo "       raw to .cfl first (see SKILL.md)." >&2; exit 1; }

echo ">> k-space dimensions (expect coils on dim 3:  X Y Z COILS ...):"
bart show -m "$KSP"
echo ">> REMINDER: ESPIRiT assumes a fully-sampled calibration region (ACS) near"
echo "   k-space center. If undersampling removed the ACS, coil maps are wrong."

if [ -n "$TRAJ" ]; then
  [ -f "${TRAJ}.cfl" ] || { echo "ERROR: trajectory ${TRAJ}.cfl not found." >&2; exit 1; }
  echo ">> Non-Cartesian path (trajectory supplied): gridded calibration + PICS -t."
  echo "   This is a sensible default; verify it suits your trajectory/data."
  bart nufft -a "$TRAJ" "$KSP" "${OUT}_adj"          # adjoint gridding -> coil images
  bart fft  -u 7 "${OUT}_adj" "${OUT}_gridksp"       # -> Cartesian k-space for calibration
  bart ecalib -r 24 "${OUT}_gridksp" "${OUT}_sens"   # ESPIRiT maps from gridded center
  bart pics -l1 -r "$REG" -t "$TRAJ" "$KSP" "${OUT}_sens" "$OUT"
else
  echo ">> Cartesian path (no trajectory): ESPIRiT + L1-wavelet PICS."
  bart ecalib -r 24 "$KSP" "${OUT}_sens"
  bart pics -l1 -r "$REG" "$KSP" "${OUT}_sens" "$OUT"
fi

echo ">> Done. Reconstructed image: ${OUT}.cfl/.hdr (coil maps: ${OUT}_sens)."
echo "   Tune -r (arg 3, default ${REG}): raise if aliasing remains, lower if"
echo "   the image looks over-smoothed."
