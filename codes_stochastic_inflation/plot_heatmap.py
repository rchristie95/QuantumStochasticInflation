import numpy as np
import mpmath as mp
import matplotlib.pyplot as plt

mp.mp.dps = 15 # Lower precision slightly for speed

# Define grid
m_over_H_vals = np.linspace(0.01, 3.0, 40)
sigma_vals = np.logspace(-2, 0, 40)
M, S = np.meshgrid(m_over_H_vals, sigma_vals)
P_eq_grid = np.zeros_like(M)
sqq_grid = np.zeros_like(M)
sqp_grid = np.zeros_like(M)
spp_grid = np.zeros_like(M)

H = 1.0 # H drops out of the purity mathematically, it only depends on m/H and sigma

print("Calculating 40x40 grids for Purity and Variances...")

for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        m_H = M[i, j]
        sigma = S[i, j]
        m = m_H * H
        
        volPhys = 6 * np.pi**2 / (sigma**3 * H**3)
        val = 9/4 - m_H**2
        nu = np.sqrt(val) if val >= 0 else 1j * np.sqrt(-val)
        
        mp_nu = mp.mpc(nu.real, nu.imag)
        mp_sigma = mp.mpf(sigma)

        h1 = complex(mp.hankel1(mp_nu, mp_sigma))
        h2 = complex(mp_sigma * mp.hankel1(mp_nu - 1, mp_sigma) + (1.5 - mp_nu) * mp.hankel1(mp_nu, mp_sigma))

        phaseFactor = np.exp(-np.pi * nu.imag)
        DQQ = phaseFactor * (3 * np.pi) / (4 * H * volPhys) * abs(h1)**2
        DQP = phaseFactor * -(3 * np.pi) / 4 * (h1.conjugate() * h2).real
        DPP = phaseFactor * (3 * np.pi * H * volPhys) / 4 * abs(h2)**2

        A12 = 1.0 / (H * volPhys)
        A21 = -(m**2 * volPhys) / H
        alpha = A12; beta = -A21
        
        sqp_eq = -DQQ / (2 * alpha)
        spp_eq = (DPP + beta * DQQ / alpha) / 6.0
        sqq_eq = (alpha * spp_eq + 3.0 * DQQ / (2 * alpha) + DQP) / beta

        det_eq = sqq_eq * spp_eq - sqp_eq**2
        P_eq = 1.0 / (2.0 * np.sqrt(det_eq))
        
        P_eq_grid[i, j] = P_eq
        sqq_grid[i, j] = sqq_eq
        sqp_grid[i, j] = sqp_eq
        spp_grid[i, j] = spp_eq

# Set LaTeX-like fonts
plt.rcParams['font.family'] = 'serif'
plt.rcParams['mathtext.fontset'] = 'cm'

# Convert variances and purity to log10
log_P_eq = np.log10(P_eq_grid + 1e-20)
log_sqq = np.log10(np.abs(sqq_grid) + 1e-20)
log_sqp = np.log10(np.abs(sqp_grid) + 1e-20)
log_spp = np.log10(np.abs(spp_grid) + 1e-20)

# Plotting Function
def plot_panel(data, label, is_log, title_label, filename, vmin=None, vmax=None, ticks=None):
    fig, ax = plt.subplots(figsize=(6, 4.5))
    
    # Use viridis for all plots (Python's equivalent to parula)
    levels = np.linspace(vmin, vmax, 100) # Increased levels for smoother rendering
    contour = ax.contourf(M, S, data, levels=levels, cmap='viridis', vmin=vmin, vmax=vmax, extend='both')
    
    # Overlay obvious, thin white isolines
    ax.contour(M, S, data, levels=15, colors='white', linewidths=0.4, alpha=0.85)
        
    if ticks is None:
        if is_log:
            ticks = [-8, -4, 0, 4, 8]
        else:
            ticks = [0.0, 0.25, 0.5, 0.75, 1.0]
        
    cbar = fig.colorbar(contour, ax=ax, ticks=ticks)
    cbar.set_label(label, fontsize=12)
    
    ax.axvline(x=1.5, color='white', linestyle='--', linewidth=1.5)
    ax.set_xlabel('Mass to Hubble Ratio ($m/H$)', fontsize=14)
    ax.set_ylabel(r'Coarse-Graining Cutoff ($\sigma$)', fontsize=14)
    ax.set_yscale('log')
    
    # Add (a), (b), (c), (d) tag in the top left corner inside the plot
    ax.text(0.05, 0.95, title_label, transform=ax.transAxes, fontsize=14, fontweight='bold', 
            verticalalignment='top', bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))
            
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

# Generate the 4 separate PDFs
plot_panel(log_P_eq, r'$\log_{10}(\gamma_{\infty})$', True, '(a)', 'heatmap_purity.pdf', vmin=-2.0, vmax=0.0, ticks=[-2, -1, 0])
plot_panel(log_sqq, r'$\log_{10}(\Delta \hat Q^2)$', True, '(b)', 'heatmap_sqq.pdf', vmin=-9.0, vmax=9.0)
plot_panel(log_sqp, r'$\log_{10}(|\Delta \hat Q \hat P|)$', True, '(c)', 'heatmap_sqp.pdf', vmin=-9.0, vmax=9.0)
plot_panel(log_spp, r'$\log_{10}(\Delta \hat P^2)$', True, '(d)', 'heatmap_spp.pdf', vmin=-9.0, vmax=9.0)

print("Saved separate LaTeX-styled PDF heatmaps!")
