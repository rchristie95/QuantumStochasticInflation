#!/usr/bin/env python3
"""Check explicit propagators and finite-time massless covariance; run after validate_paper_v3_gradients.py from the repository root."""
from pathlib import Path
import importlib.util,json
import numpy as np
import mpmath as mp
from scipy.integrate import solve_ivp
path=Path('codes_stochastic_inflation/validate_paper_v3_gradients.py')
spec=importlib.util.spec_from_file_location('check',path); mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
results=[]
for m in [0,.05,.5,1.5,2,4]:
 sig=.1;nu=mp.sqrt(mp.mpf('2.25')-mp.mpf(str(m))**2)
 def U(z):
  ph=mp.exp(1j*mp.pi*(2*nu+1)/4)
  h=ph*mp.hankel1(nu,z)
  g=ph*(z*mp.hankel1(nu-1,z)+(mp.mpf('1.5')-nu)*mp.hankel1(nu,z))
  return mp.matrix([[mp.re(h),mp.im(h)],[-mp.re(g),-mp.im(g)]])
 def fun(t,r):return (np.array([[0,1],[-m*m-sig*sig*np.exp(-2*t),-3]])@r.reshape(2,2)).ravel()
 sol=solve_ivp(fun,[0,7],np.eye(2).ravel(),t_eval=[.3,2,7],rtol=1e-12,atol=2e-14,method='DOP853')
 for i,t in enumerate(sol.t):
  R=np.array((mp.exp(-mp.mpf(str(t))*3/2)*U(mp.mpf(str(sig))*mp.exp(-mp.mpf(str(t))))*U(mp.mpf(str(sig)))**-1).tolist(),float)
  err=np.max(abs(sol.y[:,i].reshape(2,2)-R))/max(np.max(abs(R)),1e-20)
  assert err<1e-8,(m,t,err)
  results.append({'m_over_H':m,'tau':float(t),'relative_matrix_error':float(err)})
# Independent finite-duration massless covariance, including its noncanonical band commutator.
massless=[]
for sig in [.01,.1,.5]:
 D,V=mod.shell(0,sig);S=np.diag([np.sqrt(V),1/np.sqrt(V)]);Di=S@D@S.T
 def rhs(t,v):
  R=v[:4].reshape(2,2)
  return np.r_[(np.array([[0,1],[-sig**2*np.exp(-2*t),-3]])@R).ravel(),(R@Di@R.T).ravel()]
 T=4.;sol=solve_ivp(rhs,[0,T],np.r_[np.eye(2).ravel(),np.zeros(4)],rtol=1e-12,atol=1e-13,method='DOP853')
 Si=np.linalg.inv(S);got=Si@sol.y[4:,-1].reshape(2,2)@Si.T
 eps=sig*np.exp(-T)
 target=np.array([[(T+(sig**2-eps**2)/2)/(4*np.pi**2),-3/(4*sig)*(1-np.exp(-2*T))],[-3/(4*sig)*(1-np.exp(-2*T)),9*np.pi**2/(4*sig**2)*(1-np.exp(-4*T))]])
 err=np.max(abs((got-target)/target));assert err<1e-9
 massless.append({'sigma':sig,'duration':T,'covariance_max_relative_error':float(err),'band_commutator_factor':float(1-np.exp(-3*T))})
p=Path('codes_stochastic_inflation/paper_v3_gradient_validation.json'); data=json.loads(p.read_text());data['fundamental_matrix_checks']=results;data['finite_time_massless_checks']=massless;p.write_text(json.dumps(data,indent=2)+'\n')
print('18 real/imaginary-order fundamental matrix checks passed, max error:',max(r['relative_matrix_error'] for r in results))
print('3 finite-time massless covariance checks passed, max error:',max(r['covariance_max_relative_error'] for r in massless))
