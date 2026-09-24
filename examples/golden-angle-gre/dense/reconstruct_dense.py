"""Resolution-limited radial reconstruction using SigPy NUFFT and CG."""
from pathlib import Path
import json
import numpy as np
import sigpy as sp
import sigpy.mri as mr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
O=Path(__file__).resolve().parent
coord=(np.load(O.parent/'trajectory.npz')['k_adc'][[1,0]].T*.22).reshape(128,64,2)
N=sp.linop.NUFFT((64,64),coord,oversamp=2,width=6)
y,x=np.mgrid[-32:32,-32:32];disk=x*x+y*y<=30**2
F=sp.linop.FFT((64,64));B=F.H*sp.linop.Multiply((64,64),disk)*F
A=N*B
results={};reports={}
for ss in [4,2,1,0.5]:
 path=O/f'signal_metal_ss{ss}.npz'
 if not path.exists():continue
 d=np.load(path);raw=d['signal'].astype(np.complex128);scale=float(np.linalg.norm(raw)/np.sqrt(raw.size));data=raw/scale
 solver=sp.app.LinearLeastSquares(A,data,lamda=.01,max_iter=600,tol=1e-9,show_pbar=False)
 r=B(solver.run())
 r2=B(sp.app.LinearLeastSquares(A,data,x=r.copy(),lamda=.01,max_iter=200,tol=1e-9,show_pbar=False).run())
 residual=float(np.linalg.norm(N(r2)-data)/np.linalg.norm(data))
 change=float(np.linalg.norm(r2-r)/np.linalg.norm(r2))
 results[ss]=r2*scale
 reports[ss]=dict(data_relative_residual=residual,additional_iterations_image_change=change,signal_scale=scale)
 np.savez_compressed(O/f'reconstruction_ss{ss}.npz',image=r2*scale,predicted=N(r2)*scale,residual=(N(r2)-data)*scale,coord=coord)
 print(ss,reports[ss],flush=True)
report=dict(method='SigPy NUFFT + Fourier-disk constraint + L2 CG',fourier_disk_radius=30,effective_diameter_samples=60,nominal_resolution_mm=220/60,lambda_l2=.01,max_iterations=800,per_grid=reports)
if 2 in results and 4 in results:
 fine=results[2];coarse=results[4]
 report['complex_image_grid_change']=float(np.linalg.norm(fine-coarse)/np.linalg.norm(fine))
 report['magnitude_image_grid_change']=float(np.linalg.norm(abs(fine)-abs(coarse))/np.linalg.norm(abs(fine)))
 sf=np.load(O/'signal_metal_ss2.npz')['signal'];sc=np.load(O/'signal_metal_ss4.npz')['signal']
 report['signal_grid_change']=float(np.linalg.norm(sf-sc)/np.linalg.norm(sf))
if 1 in results:
 fine=results[1];coarse=results[2]
 report['1mm_to_0p5mm_magnitude_image_change']=float(np.linalg.norm(abs(fine)-abs(coarse))/np.linalg.norm(abs(fine)))
 report['1mm_to_0p5mm_complex_image_change']=float(np.linalg.norm(fine-coarse)/np.linalg.norm(fine))
 sf=np.load(O/'signal_metal_ss1.npz')['signal'];sc=np.load(O/'signal_metal_ss2.npz')['signal']
 report['1mm_to_0p5mm_signal_change']=float(np.linalg.norm(sf-sc)/np.linalg.norm(sf))
if .5 in results:
 fine=results[.5];coarse=results[1]
 report['native_voxel_quadrature_magnitude_change']=float(np.linalg.norm(abs(fine)-abs(coarse))/np.linalg.norm(abs(fine)))
 report['native_voxel_quadrature_complex_change']=float(np.linalg.norm(fine-coarse)/np.linalg.norm(fine))
 report['quadrature_check_pass']=report['native_voxel_quadrature_magnitude_change']<.05
ss=min(results);d=np.load(O/f'signal_metal_ss{ss}.npz')
ux=np.unique(d['x']);uy=np.unique(d['y']);density=np.zeros((len(uy),len(ux)))
density[np.searchsorted(uy,d['y']),np.searchsorted(ux,d['x'])]=d['ρ']
fig,ax=plt.subplots(1,1+min(2,len(results)),figsize=(5*(1+min(2,len(results))),5),layout='constrained')
ax[0].imshow(density,origin='lower',extent=[ux[0]*1000,ux[-1]*1000,uy[0]*1000,uy[-1]*1000],cmap='gray',interpolation='nearest');ax[0].set_title('Dense simulation phantom\nspin density · not GRE ground truth')
vmax=np.percentile(abs(results[ss]),99.5)
for a,grid in zip(ax[1:],sorted(results)[:2][::-1]):
 if grid in results:a.imshow(abs(results[grid]),origin='lower',extent=[-110,110,-110,110],cmap='gray',vmin=0,vmax=vmax,interpolation='nearest')
 a.set_title(f'{grid/2:g} mm simulation grid\n64 × 64 reconstruction')
for a in ax:a.set(xlim=(-110,110),ylim=(-110,110),xlabel='x (mm)',ylabel='y (mm)',aspect='equal')
fig.suptitle('Full KomaMRI Bloch simulation → SigPy reconstruction\n128 golden-angle spokes · same sequence · no display smoothing',fontsize=15)
fig.savefig(O/'dense_reconstruction.png',dpi=170);fig.savefig(O/'dense_reconstruction.pdf')
(O/'reconstruction_report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2),flush=True)
