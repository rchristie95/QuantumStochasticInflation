"""Check the displayed A_N counting and homodyne equations against GKLS.

Random pure states, Hermitian Hamiltonians and non-normal channel matrices test
the operator algebra without assuming a Gaussian state or a commuting channel.
"""
import numpy as np


def verify():
    rng=np.random.default_rng(26061029)
    residuals=[]
    for dimension in (2,4,7):
        for _ in range(12):
            a=(rng.normal(size=(dimension,dimension))+1j*rng.normal(size=(dimension,dimension)))/np.sqrt(dimension)
            raw=rng.normal(size=(dimension,dimension))+1j*rng.normal(size=(dimension,dimension))
            k=(raw+raw.conj().T)/2
            psi=rng.normal(size=dimension)+1j*rng.normal(size=dimension)
            psi/=np.linalg.norm(psi)
            rho=np.outer(psi,psi.conj());number=a.conj().T@a
            generator=-1j*(k@rho-rho@k)+3*a@rho@a.conj().T-1.5*(number@rho+rho@number)
            intensity=3*np.trace(number@rho).real
            no_count=-1j*(k@rho-rho@k)-1.5*(number@rho+rho@number)+intensity*rho
            jump=3*a@rho@a.conj().T/intensity-rho
            np.testing.assert_allclose(no_count+intensity*jump,generator,atol=5e-14)
            for phase in (0,.7,2.1):
                c=np.sqrt(3)*np.exp(1j*phase)*a
                signal=np.vdot(psi,(c+c.conj().T)@psi).real
                drift=-1j*k-1.5*number+.5*signal*c-signal**2/8*np.eye(dimension)
                noise=c-.5*signal*np.eye(dimension)
                norm_drift=2*np.vdot(psi,drift@psi).real+np.linalg.norm(noise@psi)**2
                norm_noise=2*np.vdot(psi,noise@psi).real
                assert abs(norm_drift)<5e-14 and abs(norm_noise)<5e-14
                density_drift=drift@rho+rho@drift.conj().T+noise@rho@noise.conj().T
                density_noise=noise@rho+rho@noise.conj().T
                np.testing.assert_allclose(density_drift,generator,atol=5e-14)
                np.testing.assert_allclose(density_noise,c@rho+rho@c.conj().T-signal*rho,atol=5e-14)
                residuals.append(np.max(np.abs(density_drift-generator)))
            # The pre-trace expansion has the paper's minus-sign convention.
            dt=1e-6
            m0=np.eye(dimension)-(1j*k+1.5*number)*dt
            m1=-np.sqrt(3*dt)*a
            joint=np.block([[m0@rho@m0.conj().T,m0@rho@m1.conj().T],
                            [m1@rho@m0.conj().T,m1@rho@m1.conj().T]])
            reduced=joint[:dimension,:dimension]+joint[dimension:,dimension:]
            np.testing.assert_allclose((reduced-rho)/dt,generator,atol=2e-4)
    print(f"PASS: 36 counting states, 108 homodyne states/phases, Ito norm, identical GKLS drift and block trace; max residual {max(residuals):.3g}")


if __name__=="__main__":verify()
