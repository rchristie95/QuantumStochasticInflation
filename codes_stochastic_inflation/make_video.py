"""
Open Stochastic Inflation - Fokker-Planck ODE Solver & Phase Space Visualizer

This script solves the exact 5-dimensional Gaussian equations of motion (mean Q, mean P, 
and the 3 covariance elements) for the Wigner/Fokker-Planck equation describing a scalar 
field in de Sitter space. It handles both light and heavy mass regimes using arbitrary 
precision math (mpmath) for the complex-order Hankel mode functions.

Options:
- `use_equilibrium_covariance`: If True, forces the initial state to the theoretical 
  stationary equilibrium state, removing transient dynamics.
- `only_calculate_stationary`: If True, computes the exact stationary purity and 
  covariance for the given parameters, prints them to the terminal, and exits without 
  solving the ODE or rendering the video.

Requirements: numpy, scipy, matplotlib, mpmath, imageio[ffmpeg]
"""
import numpy as np
import mpmath as mp
from scipy.integrate import solve_ivp
from scipy.stats import multivariate_normal
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import imageio_ffmpeg

plt.rcParams['animation.ffmpeg_path'] = imageio_ffmpeg.get_ffmpeg_exe()


# Parameters
sigma = 0.1
H = 10
m = 1
Nmax = 25.0
volPhys = 6 * np.pi**2 / (sigma**3 * H**3)

# Initial Conditions
q0 = 5.0
p0 = 0.0
sqq0 = 0.5
sqp0 = 0.0
spp0 = 0.5

# Options
use_equilibrium_covariance = True
only_calculate_stationary = False

# Calculate nu
val = 9/4 - (m/H)**2
if val >= 0:
    nu = np.sqrt(val)
else:
    nu = 1j * np.sqrt(-val)

# Compute Hankel functions with mpmath to support complex nu
mp.mp.dps = 25  # Set precision
mp_nu = mp.mpc(nu.real, nu.imag)
mp_sigma = mp.mpf(sigma)

h1_mp = mp.hankel1(mp_nu, mp_sigma)
h2_mp = mp_sigma * mp.hankel1(mp_nu - 1, mp_sigma) + (1.5 - mp_nu) * mp.hankel1(mp_nu, mp_sigma)

h1 = complex(h1_mp)
h2 = complex(h2_mp)

# Diffusion constants with the correct phase factor logic for heavy fields
phaseFactor = np.exp(-np.pi * nu.imag)
DQQ = phaseFactor * (3 * np.pi) / (4 * H * volPhys) * abs(h1)**2
DQP = phaseFactor * -(3 * np.pi) / 4 * (h1.conjugate() * h2).real
DPP = phaseFactor * (3 * np.pi * H * volPhys) / 4 * abs(h2)**2

A11 = 0.0
A12 = 1.0 / (H * volPhys)
A21 = -(m**2 * volPhys) / H
A22 = -3.0

# Always calculate the exact equilibrium covariance parameters
alpha = A12
beta = -A21
sqp_eq = -DQQ / (2 * alpha)
spp_eq = (DPP + beta * DQQ / alpha) / 6.0
sqq_eq = (alpha * spp_eq + 3.0 * DQQ / (2 * alpha) + DQP) / beta

# Calculate stationary purity P = 1 / (2 * sqrt(det(Sigma_eq)))
det_eq = sqq_eq * spp_eq - sqp_eq**2
stationary_purity = 1.0 / (2.0 * np.sqrt(det_eq))
print(f"Theoretical Stationary Purity: {stationary_purity:.4e}")

if only_calculate_stationary:
    print("Stationary covariance:")
    print(f"sqq = {sqq_eq:.4g}, sqp = {sqp_eq:.4g}, spp = {spp_eq:.4g}")
    print("Exiting as requested by `only_calculate_stationary` option.")
    import sys
    sys.exit(0)

if use_equilibrium_covariance:
    sqq0, sqp0, spp0 = sqq_eq, sqp_eq, spp_eq
    print("Using equilibrium covariance for initial conditions:")
    print(f"sqq0 = {sqq0:.4g}, sqp0 = {sqp0:.4g}, spp0 = {spp0:.4g}")

def equations(t, y):
    # y = [q, p, sqq, sqp, spp]
    q, p, sqq, sqp, spp = y
    dq_dt = A11 * q + A12 * p
    dp_dt = A21 * q + A22 * p
    dsqq_dt = 2 * A11 * sqq + 2 * A12 * sqp + DQQ
    dsqp_dt = A21 * sqq + (A11 + A22) * sqp + A12 * spp + DQP
    dspp_dt = 2 * A21 * sqp + 2 * A22 * spp + DPP
    return [dq_dt, dp_dt, dsqq_dt, dsqp_dt, dspp_dt]

# Calculate and print initial purity
det_initial = sqq0 * spp0 - sqp0**2
initial_purity = 1.0 / (2.0 * np.sqrt(det_initial))
print(f"Initial Purity: {initial_purity:.4e}")
print(f"Initial (Q, P): ({q0:.4e}, {p0:.4e})")

y0 = [q0, p0, sqq0, sqp0, spp0]
# Solve ODE using Radau (an implicit method ideal for stiff exponential growth)
sol = solve_ivp(equations, [0, Nmax], y0, method='Radau', rtol=1e-8, atol=1e-10, dense_output=True)

# Sample the frames for video (e.g., 200 frames total for a 10-second video at 20 fps)
num_frames = 50
t_frames = np.linspace(0, Nmax, num_frames)
y_frames = sol.sol(t_frames)

q_sol = y_frames[0]
p_sol = y_frames[1]
sqq_sol = y_frames[2]
sqp_sol = y_frames[3]
spp_sol = y_frames[4]

# Calculate and print final purity
det_final = sqq_sol[-1] * spp_sol[-1] - sqp_sol[-1]**2
final_purity = 1.0 / (2.0 * np.sqrt(det_final))
print(f"Final Purity (at N={Nmax}): {final_purity:.4e}")
print(f"Final (Q, P): ({q_sol[-1]:.4e}, {p_sol[-1]:.4e})")

max_sqq = np.max(sqq_sol)
max_spp = np.max(spp_sol)

# Dynamic padding
qRange = [np.min(q_sol) - 3 * np.sqrt(max_sqq), np.max(q_sol) + 3 * np.sqrt(max_sqq)]
pRange = [np.min(p_sol) - 3 * np.sqrt(max_spp), np.max(p_sol) + 3 * np.sqrt(max_spp)]

# Create high-resolution grid for smooth plotting
grid_res = 400
Q, P = np.meshgrid(np.linspace(qRange[0], qRange[1], grid_res),
                   np.linspace(pRange[0], pRange[1], grid_res))
pos = np.dstack((Q, P))

plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(8, 6))
fig.patch.set_facecolor('#0d0d12')
ax.set_facecolor('#0d0d12')
ax.set_xlim(qRange[0], qRange[1])
ax.set_ylim(pRange[0], pRange[1])
ax.set_xlabel('Q', fontsize=12, labelpad=10)
ax.set_ylabel('P', fontsize=12, labelpad=10)

contour = None

def update(frame):
    global contour
    if contour:
        contour.remove()
    
    t = t_frames[frame]
    mu = [q_sol[frame], p_sol[frame]]
    cov = [[sqq_sol[frame], sqp_sol[frame]], 
           [sqp_sol[frame], spp_sol[frame]]]
    
    # Add tiny regularizer
    # cov[0][0] += 1e-6
    # cov[1][1] += 1e-6
    
    rv = multivariate_normal(mu, cov, allow_singular=True)
    Z = rv.pdf(pos)
    
    # Use pcolormesh with gouraud shading for perfectly smooth, continuous gradients
    contour = ax.pcolormesh(Q, P, Z, shading='gouraud', cmap='magma')
    ax.set_title(f"Phase Space at N = {t:.2f}", fontsize=14, pad=15)
    return []

print("Generating frames and exporting video...")
ani = animation.FuncAnimation(fig, update, frames=num_frames, blit=False)
dynamic_fps = num_frames / 20.0
writer = animation.FFMpegWriter(fps=dynamic_fps, metadata=dict(artist='Antigravity'), bitrate=2500)
ani.save("phase_space_evolution_py.mp4", writer=writer)
print("Video saved to phase_space_evolution_py.mp4")
