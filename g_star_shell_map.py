import numpy as np
import math
import os
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Parameters (match those used in g_star_spiral_model_run.py)
r1_ly = 20366.0
r2_ly = 20374.0
ly_to_pc = 0.306601
r1 = r1_ly * ly_to_pc
r2 = r2_ly * ly_to_pc

R0_pc = 8122.0
Rd = 2600.0
hz = 300.0
Rmax = 15000.0

n_arms = 4
pitch_deg = 12.0
arm_half_width = 300.0

N_mc = 100000  # adjust if you want more points

# helper compute_sigma0
import math
def compute_sigma0(N_total, Rd, Rmax):
    integral = 2 * math.pi * Rd**2 * (1 - math.exp(-Rmax/Rd)*(1 + Rmax/Rd))
    return N_total / integral

# Use same default N_total_G as used earlier
N_total_G = 2.0e10
sigma0 = compute_sigma0(N_total_G, Rd, Rmax)

# build arm params (fallback parametric arms)
pitch = math.radians(pitch_deg)
r_ref = R0_pc
phi0 = 0.0
arm_params = []
for k in range(n_arms):
    phi_ref_k = phi0 + k * (2.0*math.pi / n_arms)
    arm_params.append(dict(name=f'arm{k+1}', R_ref=r_ref, phi_ref=phi_ref_k, pitch=pitch))

# Monte Carlo sample points uniformly in shell volume
u = np.random.uniform(r1**3, r2**3, size=N_mc)
r = u ** (1.0/3.0)
cos_theta = np.random.uniform(-1.0, 1.0, size=N_mc)
theta = np.arccos(cos_theta)
phi = np.random.uniform(0.0, 2.0*math.pi, size=N_mc)

# positions in Sun-centered Cartesian coordinates (pc)
x_sun = r * np.sin(theta) * np.cos(phi)
y_sun = r * np.sin(theta) * np.sin(phi)
z_sun = r * cos_theta

# convert to Galactocentric coordinates: place Sun at (R0, 0, 0)
X_gc = R0_pc + x_sun
Y_gc = y_sun
Z_gc = z_sun

R_gc = np.sqrt(X_gc**2 + Y_gc**2)
phi_gc = np.arctan2(Y_gc, X_gc)

# Determine arm membership using a local phi window search for minimal radial separation
phi_window_half = math.radians(6.0)
n_phi_samples = 121
phi_offsets = np.linspace(-phi_window_half, phi_window_half, n_phi_samples)
sep_min = np.full(N_mc, np.inf)
for arm in arm_params:
    R_ref = arm['R_ref']
    phi_ref = arm['phi_ref']
    pitch = arm['pitch']
    tan_p = math.tan(pitch)
    phi_grid = (phi_gc[:, None] + phi_offsets[None, :])
    phi_rel = (phi_grid - phi_ref + math.pi) % (2.0*math.pi) - math.pi
    R_arm_grid = R_ref * np.exp(phi_rel * tan_p)
    radial_sep_grid = np.abs(R_gc[:, None] - R_arm_grid)
    sep_min = np.minimum(sep_min, np.min(radial_sep_grid, axis=1))

in_arm = sep_min < arm_half_width

# Save CSV of points that are in arms
import csv
out_csv = 'g_shell_in_arm_positions.csv'
with open(out_csv, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['X_gc_pc','Y_gc_pc','Z_gc_pc','R_gc_pc','in_arm'])
    for i in range(N_mc):
        writer.writerow([f'{X_gc[i]:.6f}', f'{Y_gc[i]:.6f}', f'{Z_gc[i]:.6f}', f'{R_gc[i]:.6f}', int(in_arm[i])])

# Make plot
fig, ax = plt.subplots(figsize=(8,8))
# plot all points faint
ax.scatter(X_gc, Y_gc, s=1, c='lightgray', alpha=0.6, label='sampled points')
# plot in-arm points
ax.scatter(X_gc[in_arm], Y_gc[in_arm], s=2, c='red', alpha=0.6, label='in arms (sampled)')

# plot arm centerlines
phi_line = np.linspace(-math.pi, math.pi, 2000)
for arm in arm_params:
    R_ref = arm['R_ref']
    phi_ref = arm['phi_ref']
    tan_p = math.tan(arm['pitch'])
    phi_rel = (phi_line - phi_ref + math.pi) % (2.0*math.pi) - math.pi
    R_arm = R_ref * np.exp(phi_rel * tan_p)
    X_arm = R_arm * np.cos(phi_line)
    Y_arm = R_arm * np.sin(phi_line)
    ax.plot(X_arm, Y_arm, '-', linewidth=1.0, alpha=0.9)

# Mark Galactic center and Sun
ax.scatter(0, 0, c='k', s=30, marker='*', label='Galactic center')
ax.scatter(R0_pc, 0, c='blue', s=20, marker='o', label='Sun location')

ax.set_aspect('equal')
ax.set_xlabel('X (pc)')
ax.set_ylabel('Y (pc)')
ax.set_title('G-type stars: sampled shell positions and arm membership (Galactocentric view)')
ax.legend(loc='upper right', fontsize='small')

# set limits to show region around Sun and arms
lim = R0_pc + (r2 + 1000)
ax.set_xlim(-lim, lim)
ax.set_ylim(-lim, lim)

out_png = 'g_star_shell_arms.png'
plt.savefig(out_png, dpi=200, bbox_inches='tight')
plt.close()

# Also write a small JSON summary
summary = dict(V_shell=(4.0/3.0)*math.pi*(r2**3 - r1**3), N_mc=N_mc, N_in_arm=int(np.sum(in_arm)), frac_in_arm=float(np.mean(in_arm)))
with open('g_shell_map_summary.json','w') as f:
    json.dump(summary, f, indent=2)

print(f'Wrote: {out_png}, {out_csv}, and g_shell_map_summary.json')
