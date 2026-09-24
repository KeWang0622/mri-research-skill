"""KomaMRI quadrature refinement within fixed native 0.5-mm tissue voxels."""
from pathlib import Path
import time,json
import numpy as np
import komamripy as km
O=Path(__file__).resolve().parent
km.load_metal()
scanner=km.Scanner(limits=km.HardwareLimits(Gmax=.032,Smax=130.))
seq=km.files.read_seq(str(O.parent/'golden_angle_radial_gre.seq'))
params={'return_type':'mat','gpu':True,'precision':'f32','Δt_rf':5e-6,'Δt':10e-6}
d=np.load(O/'signal_metal_ss1.npz');fields={n:d[n].copy() for n in ['x','y','ρ','T1','T2','T2s','Δw']}
z=np.linspace(-.004,.004,33);dz=z[1]-z[0];wz=np.ones(33);wz[[0,-1]]=.5
base={n:np.tile(a,33) for n,a in fields.items()};base['ρ']*=np.repeat(wz,len(fields['x']))*.0005**2*dz;base['z']=np.repeat(z,len(fields['x']))
signals=[];start=time.time()
for i,(sx,sy) in enumerate([(-1,-1),(-1,1),(1,-1),(1,1)]):
 path=O/f'subvoxel_{i}.npy'
 if path.exists():signals.append(np.load(path));continue
 kw=dict(base);kw['x']=base['x']+sx*.000125;kw['y']=base['y']+sy*.000125
 obj=km.Phantom(name=f'native_voxel_quadrature_{i}',**kw)
 print('START subvoxel',i,flush=True)
 raw=np.asarray(km.simulate(obj,seq,scanner,sim_params=params)).copy().reshape(128,64)
 assert np.isfinite(raw).all()
 np.save(path,raw);signals.append(raw)
 print('DONE subvoxel',i,flush=True)
# Linearity across independent spins: sum four equal subvoxel volumes.
signal=np.mean(np.asarray(signals,dtype=np.complex128),axis=0)
np.savez_compressed(O/'signal_metal_ss0.5.npz',signal=signal,**fields)
(O/'simulation_subvoxel.json').write_text(json.dumps(dict(engine='KomaMRI Metal f32',native_tissue_map_mm=.5,quadrature_spacing_mm=.25,quadrature_points=4*len(base['x']),seconds=time.time()-start,assumption='Piecewise constant tissue parameters within each native 0.5-mm voxel; four equally weighted samples at +/-0.125 mm in x/y. No added anatomical detail.'),indent=2))
