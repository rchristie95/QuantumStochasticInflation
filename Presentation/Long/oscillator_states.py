"""Discrete average/total oscillator channel and actual conditional Wigner grids.

No free dynamics between additions. hbar=1; Q_n=sum(q_j)/n, P_n=sum(p_j).
Number readout is in the Fock basis of (R,P_R); Q readout measures R ideally.
The selected records are illustrative possible records, not typical ensembles.
"""
from functools import lru_cache
from pathlib import Path
import hashlib
import json

import numpy as np
from PIL import Image
from scipy.interpolate import CubicSpline, RegularGridInterpolator

Q = np.linspace(-6,6,301)
R = np.linspace(-8,8,801)
DQ = Q[1]-Q[0]
DR = R[1]-R[0]
FOCK_RECORD = (1,0,1,0,0,0)
POSITION_RECORD = (.8,-.6,.5,-.4,.3,-.2)


def gaussian_wave(q, variance):
    return (2*np.pi*variance)**(-.25)*np.exp(-q*q/(4*variance))


def canonical_map(n, fraction=1.):
    """Symplectic path: balanced orthogonal mixing plus canonical rescaling.

    At fraction=0 the fresh mode has a fixed parity reflection. Its incoming
    squeezed vacuum is even, so the initial state is unchanged. This convention
    produces R=Q_n-q_new rather than its negative, continuously and canonically.
    """
    t=fraction
    angle=t*np.arctan(1/np.sqrt(n))
    rotation=np.array([[np.cos(angle),np.sin(angle)],
                       [np.sin(angle),-np.cos(angle)]])
    a=np.diag([(n+1)**(-t/2),((n+1)/n)**(t/2)])@rotation@np.diag([n**(t/2),1])
    b=np.linalg.inv(a).T
    return np.block([[a,np.zeros((2,2))],[np.zeros((2,2)),b]])


def joint_wave(psi,n):
    q,r=np.meshgrid(Q,R,indexing='ij')
    old=q+r/(n+1)
    fresh=q-n*r/(n+1)
    value=CubicSpline(Q,psi,extrapolate=False)(old)
    return np.nan_to_num(value)*gaussian_wave(fresh,.25)


def fock_basis(count=48):
    basis=np.zeros((count,len(R)))
    basis[0]=np.pi**(-.25)*np.exp(-R*R/2)
    basis[1]=np.sqrt(2)*R*basis[0]
    for m in range(1,count-1):
        basis[m+1]=np.sqrt(2/(m+1))*R*basis[m]-np.sqrt(m/(m+1))*basis[m-1]
    return basis


def fock_branches(psi,n):
    joint=joint_wave(psi,n)
    amplitudes=joint@(fock_basis().T*DR)
    probabilities=np.sum(np.abs(amplitudes)**2,axis=0)*DQ
    return amplitudes,probabilities,joint


def position_branch(psi,n,outcome):
    old=Q+outcome/(n+1)
    fresh=Q-n*outcome/(n+1)
    values=np.nan_to_num(CubicSpline(Q,psi,extrapolate=False)(old))*gaussian_wave(fresh,.25)
    density=float(np.sum(np.abs(values)**2)*DQ)
    return values/np.sqrt(density),density


def pure_wigner(psi,fft_size=2048):
    """W(q,p)=pi^-1 int dy exp(2ipy) psi(q-y) psi*(q+y)."""
    corr=np.zeros((len(Q),fft_size),dtype=complex)
    for i in range(len(Q)):
        k=np.arange(-min(i,len(Q)-1-i),min(i,len(Q)-1-i)+1)
        corr[i,k%fft_size]=psi[i-k]*np.conj(psi[i+k])
    w=np.fft.fftshift(np.fft.ifft(corr,axis=1),axes=1).real*fft_size*DQ/np.pi
    p=np.fft.fftshift(np.fft.fftfreq(fft_size,d=DQ))*np.pi
    return p,w


def master_covariance(n):
    return np.diag([(1+(n-1)/4)/n**2,.25+n-1])


@lru_cache(maxsize=1)
def trajectories():
    psi0=gaussian_wave(Q,1.)
    rows=[dict(n=1,master=master_covariance(1),fock=psi0.copy(),position=psi0.copy(),
               fock_outcome=None,fock_probability=None,position_outcome=None,position_density=None)]
    fock=psi0.copy();position=psi0.copy()
    for n,(m,r) in enumerate(zip(FOCK_RECORD,POSITION_RECORD),1):
        amplitudes,probabilities,_=fock_branches(fock,n)
        probability=float(probabilities[m])
        fock=amplitudes[:,m]/np.sqrt(probability)
        position,density=position_branch(position,n,r)
        rows.append(dict(n=n+1,master=master_covariance(n+1),fock=fock.copy(),position=position.copy(),
                         fock_outcome=m,fock_probability=probability,fock_completeness=float(probabilities.sum()),
                         position_outcome=r,position_density=density))
    return rows


def make_assets(folder):
    """Scientific raster grids; fixed Q/P axes and fixed signed colour scale."""
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    fingerprint=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    manifest=folder/'manifest.json'
    if manifest.exists():
        cached=json.loads(manifest.read_text())
        if cached.get('source_sha256')==fingerprint and all((folder/f'{kind}-{n}.png').exists() for kind in ('master','fock','position') for n in range(1,8)):
            return cached
    q=np.linspace(-3,3,401);p=np.linspace(-8,8,401)
    xx,yy=np.meshgrid(q,p,indexing='ij')
    bg=np.array([16,24,36.]);positive=np.array([102,183,255.]);negative=np.array([255,181,105.])
    metadata=[]
    for row in trajectories():
        entry={k:v for k,v in row.items() if k not in ('master','fock','position')}
        entry['master_purity']=float(1/(2*np.sqrt(np.linalg.det(row['master']))))
        for kind in ('master','fock','position'):
            if kind=='master':
                cov=row['master']
                w=np.exp(-.5*(xx*xx/cov[0,0]+yy*yy/cov[1,1]))/(2*np.pi*np.sqrt(np.linalg.det(cov)))
            else:
                momentum,grid=pure_wigner(row[kind])
                w=RegularGridInterpolator((Q,momentum),grid,bounds_error=False,fill_value=0)(np.stack([xx,yy],axis=-1))
            # Flip P vertically for image coordinates; common W scale +/-1/pi.
            values=np.flipud(w.T)
            strength=np.clip(np.abs(values)*np.pi,0,1)[...,None]
            rgb=bg+(np.where(values[...,None]>=0,positive,negative)-bg)*strength
            Image.fromarray(np.rint(rgb).astype('uint8')).save(folder/f'{kind}-{row["n"]}.png')
        metadata.append(entry)
    result=dict(source_sha256=fingerprint,rows=metadata,axes=dict(Q=[-3,3],P=[-8,8]),wigner_limit=float(1/np.pi))
    manifest.write_text(json.dumps(result,indent=2))
    return result


if __name__=='__main__':
    print(json.dumps(make_assets(Path(__file__).parent/'assets'/'oscillator_wigner'),indent=2))
