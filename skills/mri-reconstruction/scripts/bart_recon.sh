#!/usr/bin/env bash
#
# Parallel-imaging + compressed-sensing MRI reconstruction with BART.
#
# Usage:
#   bart_recon.sh <kspace_cfl_basename> <output_basename> [l1_reg]
#
# Input:  a BART .cfl/.hdr k-space file (dims: X Y Z COILS ...).
#         Convert vendor/ISMRMRD raw to .cfl first (see SKILL.md).
# Output: <output_basename>.cfl/.hdr (the reconstructed image) and
#         <output_basename>_sens.cfl/.hdr (the ESPIRiT coil maps).
#
# Requires BART on PATH: https://mrirecon.github.io/bart/
set -euo pipefail

KSP="${1:?usage: bart_recon.sh <kspace_cfl_basename> <output_basename> [l1_reg]}"
OUT="${2:?usage: bart_recon.sh <kspace_cfl_basename> <output_basename> [l1_reg]}"
REG="${3:-0.01}"   # L1-wavelet regularization strength

if ! command -v bart >/dev/null 2>&1; then
  echo "ERROR: BART not found on PATH. Install it from https://mrirecon.github.io/bart/" >&2
  exit 1
fi
if [ ! -f "${KSP}.cfl" ] || [ ! -f "${KSP}.hdr" ]; then
  echo "ERROR: expected BART files ${KSP}.cfl and ${KSP}.hdr (a k-space dataset)." >&2
  echo "       Convert vendor/ISMRMRD raw to .cfl first (see SKILL.md)." >&2
  exit 1
fi

echo ">> k-space dimensions:"
bart show -m "$KSP" || true

echo ">> [1/2] ESPIRiT coil-sensitivity calibration (bart ecalib -r 24)"
bart ecalib -r 24 "$KSP" "${OUT}_sens"

echo ">> [2/2] PI+CS reconstruction (bart pics -l1 -r ${REG})"
bart pics -l1 -r "$REG" "$KSP" "${OUT}_sens" "$OUT"

echo ">> Done. Reconstructed image: ${OUT}.cfl/.hdr"
echo "   Tip: adjust the regularization (arg 3, default ${REG}) — raise it if"
echo "   residual aliasing remains, lower it if the image looks over-smoothed."
