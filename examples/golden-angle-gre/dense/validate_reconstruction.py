"""Independent analytic phase test and resolution-matched image recovery test."""
from pathlib import Path
import json
import numpy as np
import sigpy as sp
O=Path(__file__).resolve().parent
c=(np.load(O.parent/'trajectory.npz')['k_adc'][[1,0]].T*.22).reshape(128,64,2)
N=sp.linop.NUFFT((64,64),c,oversamp=2,width=6)
point=np.zeros((64,64),complex);point[21,39]=1
expected=np.exp(-2j*np.pi*(c[...,0]*(-11)+c[...,1]*7)/64)/64
point_err=float(np.linalg.norm(N(point)-expected)/np.linalg.norm(expected))
y,x=np.mgrid[-32:32,-32:32];disk=x*x+y*y<=30**2
F=sp.linop.FFT((64,64));B=F.H*sp.linop.Multiply((64,64),disk)*F
original=sp.shepp_logan((64,64));truth=B(original)
A=N*B
rec=sp.app.LinearLeastSquares(A,A(truth),max_iter=1500,tol=1e-11,show_pbar=False).run()
rec=B(rec)
err=float(np.linalg.norm(rec-truth)/np.linalg.norm(truth))
r=dict(point_phase_axis_relative_error=point_err,resolution_matched_image_error=err,excluded_high_frequency_energy_norm=float(np.linalg.norm(truth-original)/np.linalg.norm(original)),reference='Shepp-Logan projected to a Fourier disk of radius 30 grid units; original sharp phantom is NOT the reconstruction target',iterations_max=1500,pass_phase=point_err<1e-4,pass_image=err<.01)
(O/'validation.json').write_text(json.dumps(r,indent=2))
np.savez_compressed(O/'validation.npz',original=original,truth=truth,recovered=rec)
print(json.dumps(r,indent=2))
