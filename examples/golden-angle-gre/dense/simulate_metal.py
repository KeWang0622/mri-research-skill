"""Grid-refinement experiment using the existing sequence and KomaMRI."""
from pathlib import Path
import time,json
import numpy as np
import komamripy as km
O=Path(__file__).resolve().parent
km.load_metal()
scanner=km.Scanner(limits=km.HardwareLimits(Gmax=.032,Smax=130.))
seq=km.files.read_seq(str(O.parent/'golden_angle_radial_gre.seq'))
params={'return_type':'mat','gpu':True,'precision':'f32','Δt_rf':5e-6,'Δt':10e-6}
for ss in [4,2,1]:
 if (O/f'signal_metal_ss{ss}.npz').exists(): continue
 base=km.brain_phantom2D(ss=ss)
 fields={n:np.asarray(getattr(base,n),dtype=float).copy() for n in ['x','y','ρ','T1','T2','T2s','Δw']}
 z=np.linspace(-.004,.004,33)
 dx=float(np.median(np.diff(np.unique(fields['x']))));dy=float(np.median(np.diff(np.unique(fields['y']))))
 dz=z[1]-z[0]
 kw={n:np.tile(a,len(z)) for n,a in fields.items()}
 # Quadrature volume weighting: comparable physical signal across grids.
 wz=np.ones(len(z));wz[[0,-1]]=.5
 kw['ρ']*=np.repeat(wz,len(fields['x']))*dx*dy*dz
 kw['z']=np.repeat(z,len(fields['x']))
 obj=km.Phantom(name=f'brain_ss{ss}_z33',**kw)
 print('START',ss,len(kw['x']),dx,dy,flush=True)
 start=time.time()
 raw=np.asarray(km.simulate(obj,seq,scanner,sim_params=params)).copy().reshape(128,64)
 assert np.isfinite(raw).all() and np.max(abs(raw))>0
 np.savez_compressed(O/f'signal_metal_ss{ss}.npz',signal=raw,**fields)
 report=dict(backend='Metal',precision='f32',ss=ss,spins=len(kw['x']),in_plane_spins=len(fields['x']),dx_mm=dx*1000,dy_mm=dy*1000,z_positions=33,z_step_mm=dz*1000,seconds=time.time()-start,rf_step_us=5,gradient_step_us=10)
 (O/f'simulation_metal_ss{ss}.json').write_text(json.dumps(report,indent=2))
 print('DONE',json.dumps(report),flush=True)
