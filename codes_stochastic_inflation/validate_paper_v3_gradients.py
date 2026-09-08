#!/usr/bin/env python3
"""Independent mode/window and shell-propagator checks for paper_v3.
Run from the repository root: python3 codes_stochastic_inflation/validate_paper_v3_gradients.py
Uses H=a=1; results retain the paper's extensive canonical momentum.
"""
import json
from pathlib import Path
import mpmath as mp
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.linalg import solve_continuous_lyapunov

mp.mp.dps = 40
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'codes_stochastic_inflation' / 'paper_v3_gradient_validation.json'

def mode(m, z):
    nu = mp.sqrt(mp.mpf('2.25') - mp.mpf(str(m))**2)
    phase = mp.exp(1j*mp.pi*(2*nu+1)/4)
    f = mp.sqrt(mp.pi)/2*phase*mp.hankel1(nu, z)
    p = -mp.sqrt(mp.pi)/2*phase*(z*mp.hankel1(nu-1,z)+(mp.mpf('1.5')-nu)*mp.hankel1(nu,z))
    return f, p

def exact_cov(m, sigma):
    sig = mp.mpf(str(sigma)); vol = 6*mp.pi**2/sig**3
    nu = mp.sqrt(mp.mpf('2.25')-mp.mpf(str(m))**2)
    power = 1/(3-2*mp.re(nu))
    def entry(t, ij):
        z = sig*t**power
        f,p = mode(m,z)
        vals = [abs(f)**2, vol*mp.re(mp.conj(f)*p), vol**2*abs(p)**2]
        return power*sig**3*t**(3*power-1)*vals[ij]/(2*mp.pi**2)
    vals = [mp.quad(lambda t: entry(t,ij), [0, mp.mpf('.5'),mp.mpf('.9'),1]) for ij in range(3)]
    return mp.matrix([[vals[0],vals[1]],[vals[1],vals[2]]])

def shell(m,sigma):
    sig = mp.mpf(str(sigma)); vol = 6*mp.pi**2/sig**3
    f,p=mode(m,sig)
    wr = f*mp.conj(p)-mp.conj(f)*p
    assert abs(wr-1j)<mp.mpf('1e-30')
    D=mp.matrix([[3*abs(f)**2/vol,3*mp.re(mp.conj(f)*p)], [3*mp.re(mp.conj(f)*p),3*vol*abs(p)**2]])
    assert abs(mp.det(D)-mp.mpf('2.25'))<mp.mpf('1e-25')
    return np.array(D.tolist(),dtype=float),float(vol)

def homogeneous_cov_mpf(m,sigma):
    sig=mp.mpf(str(sigma)); mass=mp.mpf(str(m)); vol=6*mp.pi**2/sig**3
    f,p=mode(m,sig)
    dqq=3*abs(f)**2/vol; dqp=3*mp.re(mp.conj(f)*p); dpp=3*vol*abs(p)**2
    qp=-vol*dqq/2
    pp=(dpp+mass**2*vol**2*dqq)/6
    qq=(pp/vol-3*qp+dqp)/(mass**2*vol)
    return mp.matrix([[qq,qp],[qp,pp]])

def propagation_cov(m,sigma,D,vol,stop=20):
    # Symplectic scaling balances numerical components, while preserving det Sigma.
    S=np.diag([np.sqrt(vol),1/np.sqrt(vol)])
    Di=S@D@S.T
    A=np.array([[0,1],[-m*m,-3.]])
    def rhs(t,v):
        R=v[:4].reshape(2,2)
        At=A.copy(); At[1,0]-=sigma*sigma*np.exp(-2*t)
        return np.r_[(At@R).ravel(),(R@Di@R.T).ravel()]
    sol=solve_ivp(rhs,[0,stop],np.r_[np.eye(2).ravel(),np.zeros(4)],method='DOP853',rtol=2e-12,atol=2e-13)
    assert sol.success
    R=sol.y[:4,-1].reshape(2,2)
    first=sol.y[4:,-1].reshape(2,2)
    # Beyond stop, gradients are <= sigma^2 exp(-2 stop). This tail is
    # checked by moving stop from 20 to 24, not used in the direct integral.
    total=first+solve_continuous_lyapunov(A,-R@Di@R.T)
    hom=solve_continuous_lyapunov(A,-Di)
    Si=np.linalg.inv(S)
    return Si@total@Si.T,Si@hom@Si.T

def symbolic_checks():
    y=sp.symbols('y',positive=True)
    def inner(f,g):return sp.integrate(sp.Rational(3,2)*sp.sqrt(y)*f*g,(y,0,1))
    fs=[]
    for n in range(5):
        f=y**n
        for g in fs:f-=inner(f,g)*g
        fs.append(sp.simplify(f/sp.sqrt(inner(f,f))))
    T=sp.Matrix(5,5,lambda i,j:inner(-2*y*sp.diff(fs[i],y),fs[j]))
    M=sp.Matrix(5,5,lambda i,j:inner(fs[i],y*fs[j]))
    b=sp.Matrix([f.subs(y,1) for f in fs])
    assert sp.simplify(T+T.T-3*sp.eye(5)+3*b*b.T)==sp.zeros(5)
    assert M==M.T and M[0,0]==sp.Rational(3,5)
    assert sp.simplify(fs[1]-sp.sqrt(sp.Rational(175,12))*(y-sp.Rational(3,5)))==0
    # Derive massless pi from a derivative, then integrate all covariance terms.
    k,a,H,sig=sp.symbols('k a H sigma',positive=True)
    u=H/sp.sqrt(2*k**3)*(1-sp.I*k/(a*H))*sp.exp(sp.I*k/(a*H))
    p=sp.simplify(a**4*H*sp.diff(u,a))
    vol=6*sp.pi**2/(sig*a*H)**3; measure=k**2/(2*sp.pi**2)
    upper=sig*a*H
    pp=sp.simplify(sp.integrate(measure*vol**2*sp.expand_complex(p*sp.conjugate(p)),(k,0,upper)))
    qp=sp.simplify(sp.integrate(measure*vol*sp.re(sp.expand_complex(sp.conjugate(u)*p)),(k,0,upper)))
    force=-vol*a*k**2*u/H
    pf=sp.simplify(sp.integrate(measure*2*sp.re(sp.expand_complex(sp.conjugate(vol*p)*force)),(k,0,upper)))
    assert pp==9*sp.pi**2/(4*H**2*sig**2)
    assert qp==-3/(4*sig) and sp.simplify(pf-2*pp)==0
    return {'canonical_polynomials':5,'commutator_balance':'exact','massless_PP':str(pp),'massless_QP':str(qp),'massless_gradient_balance':'exact'}

def main():
    result={'symbolic':symbolic_checks(),'massive':[]}
    cases=[(.05,.1),(.5,.1),(1.,.1),(1.5,.1),(2.,.1),(4.,.1),(1.5,.01),(2.,.01),(.05,.01)]
    for m,sig in cases:
        exact=exact_cov(m,sig)
        D,vol=shell(m,sig)
        prop,hom=propagation_cov(m,sig,D,vol)
        prop24,_=propagation_cov(m,sig,D,vol,24)
        target=np.array(exact.tolist(),dtype=float)
        err=float(np.max(np.abs((prop-target)/np.maximum(np.abs(target),1e-30))))
        tail=float(np.max(np.abs((prop24-prop)/np.maximum(np.abs(target),1e-30))))
        assert err<3e-8,(m,sig,err)
        assert tail<3e-8,(m,sig,tail)
        hom_mp=homogeneous_cov_mpf(m,sig)
        hom=np.array(hom_mp.tolist(),dtype=float)
        purity=float(1/(2*mp.sqrt(mp.det(exact))))
        assert 0<purity<=1+1e-12
        row={'m_over_H':m,'sigma':sig,'window_covariance':target.tolist(), 'homogeneous_covariance':hom.tolist(),'window_purity':purity,'homogeneous_purity':float(1/(2*mp.sqrt(mp.det(hom_mp)))),'PP_window_over_homogeneous':float(target[1,1]/hom[1,1]),'propagation_max_relative_error':err,'tail_check_max_relative_change':tail}
        result['massive'].append(row)
        print(json.dumps(row),flush=True)
    OUT.write_text(json.dumps(result,indent=2)+'\n')
    print(f'All checks passed; wrote {OUT}',flush=True)
if __name__=='__main__':main()
