# Raw-data formats, vendor conversion, and datasets

Use this when the user has (or wants) raw MR data: to identify a vendor format,
convert it to something workable, or find an open dataset. Always respect each
dataset's license / data-use agreement (see ground rules in SKILL.md).

## The interchange standard: ISMRMRD

**ISMRMRD** (ISMRM Raw Data format) is the vendor-neutral raw k-space container
the community standardizes on: an XML header (acquisition parameters, encoding,
coils) plus HDF5 datasets of the acquisitions. Convert vendor raw → ISMRMRD,
then read it from any toolbox (BART, SigPy, MRIReco.jl, Gadgetron).

- Spec & C/C++ API: https://github.com/ismrmrd/ismrmrd
- Python API: https://github.com/ismrmrd/ismrmrd-python
- Python tools/utilities: https://github.com/ismrmrd/ismrmrd-python-tools
- Viewer: https://github.com/ismrmrd/ismrmrdviewer

## Vendor raw formats and how they differ

Each scanner vendor writes its own proprietary raw format. Practical
orientation (details vary by software baseline/version):

- **Siemens — "twix" / `.dat`** (meas.dat, VB/VD/VE baselines). Contains raw
  ADC data + a large embedded protocol header. Read with the community
  `mapVBVD` (MATLAB) or `pymapVBVD`/`twixtools` (Python), or convert to
  ISMRMRD: https://github.com/ismrmrd/siemens_to_ismrmrd
- **GE — "P-file" (`P#####.7`)** plus, on modern systems, ScanArchive
  (`.h5`). Vendor SDK is **Orchestra**. Convert to ISMRMRD:
  https://github.com/ismrmrd/ge_to_ismrmrd (GE's fork:
  https://github.com/GEHealthCare, formerly `mrirecon`-adjacent tooling).
- **Philips — raw is a triplet `.raw` / `.lab` / `.sin`** (data, labels,
  scan-info) — sometimes also `.cpx`/`.data`/`.list`. Convert to ISMRMRD:
  https://github.com/ismrmrd/philips_to_ismrmrd
- **Bruker (preclinical)** — `fid` / `2dseq` with `method`/`acqp` parameter
  files (ParaVision). Often handled via BrkRaw or vendor tools.

Rule of thumb when a user shows you a raw file: identify the vendor from the
extension/structure, convert to ISMRMRD with the matching converter above, then
reconstruct with the toolbox of their choice (`tools.md`). If they only need
the trajectory/sampling, that lives in the sequence (`sequences-and-
trajectories.md`).

## Open datasets (mind the license/DUA)

- **mridata.org** — http://mridata.org — open archive of multi-vendor raw
  k-space (knee, brain, …), auto-converted to ISMRMRD, with parameters and
  thumbnails. Source: https://github.com/mikgroup/mridata . Basic recon
  scripts: https://github.com/MRSRL/mridata-recon . Per-dataset terms apply.
- **fastMRI** (NYU Langone + FAIR) — the large-scale benchmark: knee (~1.5k raw
  + 10k DICOM), brain (~7k), plus **prostate** and **breast** expansions. Raw
  k-space + DICOM. **Requires a signed data-use agreement / application.**
  - Apply / download: https://fastmri.med.nyu.edu  ·  Project: https://fastmri.org
  - Code & models: https://github.com/facebookresearch/fastMRI
  - Also mirrored on the AWS Open Data registry (still under the fastMRI DUA).
  - Extra labels: https://github.com/microsoft/fastmri-plus ;
    prostate: https://github.com/cai2r/fastMRI_prostate
- **OCMR** — open cardiovascular multi-coil k-space (real-time cardiac):
  https://ocmr.info . Good for dynamic/non-Cartesian cardiac recon.
- Do NOT help bypass any access gate. If a user lacks access, point them to the
  official application and to fully-open alternatives (mridata.org, OCMR).

## Getting from raw to image (sanity pipeline)

1. Convert vendor raw → ISMRMRD (or load the provided `.h5`).
2. Read k-space + trajectory + coil data (BART `ismrmrd` import, SigPy, or
   MRIReco.jl).
3. Estimate coil sensitivities (ESPIRiT: BART `ecalib` / SigPy `EspiritCalib`).
4. Reconstruct (FFT/NUFFT for fully sampled; PICS/CS/DL for undersampled — see
   `recon-methods.md` and `tools.md`).
5. Coil-combine and inspect. Watch for FOV/orientation and readout-oversampling
   conventions, which differ by vendor.
