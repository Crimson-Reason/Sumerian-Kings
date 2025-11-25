"""
G-star spiral-arm model with 1M samples for high-precision statistics.
Re-run of g_star_spiral_model_run.py with N_mc = 1,000,000 for tighter Monte Carlo error bars.
"""

import numpy as np
import math
import os
import json
import csv

# Shell geometry (Earth-centered)
r1_ly = 16408.70211 #lower radius in light-years
r2_ly = 16428.70211 #upper radius in light-years
r1 = r1_ly * 0.306601  # convert to pc
r2 = r2_ly * 0.306601  # convert to pc

# Sun's galactocentric radius (pc)
R0_pc = 8122.0

# Disk model (G stars)
Rd = 2600.0  # scale length (pc)
hz = 300.0  # vertical scale height (pc)
Rmax = 15000.0  # effective disk radius (pc)

# Spiral arms
n_arms = 4
pitch_deg = 12.0
arm_half_width = 300.0  # radial half-width (pc)

# Population
N_total_G = 2.0e10  # nominal total G stars in Milky Way

# ***** INCREASED SAMPLE SIZE *****
N_mc = 1000000  # 1 million samples for high precision

# ===== Helper: compute sigma0 =====
def compute_sigma0(N_total, Rd, Rmax):
    integral = 2 * math.pi * Rd**2 * (1 - math.exp(-Rmax/Rd)*(1 + Rmax/Rd))
    return N_total / integral

sigma0 = compute_sigma0(N_total_G, Rd, Rmax)

# ===== Load Reid arms from CSV =====
arm_params = []
use_reid_csv = os.path.exists('reid_arms.csv')
if use_reid_csv:
    try:
        with open('reid_arms.csv', newline='') as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            for row in reader:
                if len(row) < 4:
                    continue
                name = row[0]
                R_ref = float(row[1])
                phi_ref = math.radians(float(row[2]))
                pitch = math.radians(float(row[3]))
                arm_params.append(dict(name=name, R_ref=R_ref, phi_ref=phi_ref, pitch=pitch))
        print('Loaded arm parameters from reid_arms.csv')
    except Exception as e:
        print('Failed to read reid_arms.csv, falling back to parametric arms:', e)
        arm_params = []

# fallback parametric arms
if not arm_params:
    pitch = math.radians(pitch_deg)
    r_ref = R0_pc
    phi0 = 0.0
    for k in range(n_arms):
        phi_ref_k = phi0 + k * (2.0*math.pi / n_arms)
        arm_params.append(dict(name=f'arm{k+1}', R_ref=r_ref, phi_ref=phi_ref_k, pitch=pitch))

# ===== Monte Carlo: sample shell volume =====
print(f"Sampling {N_mc} points in the shell...")
u = np.random.uniform(r1**3, r2**3, size=N_mc)
r = u ** (1.0/3.0)
cos_theta = np.random.uniform(-1.0, 1.0, size=N_mc)
theta = np.arccos(cos_theta)
phi = np.random.uniform(0.0, 2.0*math.pi, size=N_mc)

# Sun-centered Cartesian (pc)
x_sun = r * np.sin(theta) * np.cos(phi)
y_sun = r * np.sin(theta) * np.sin(phi)
z_sun = r * cos_theta

# Galactocentric cylindrical
X_gc = R0_pc + x_sun
Y_gc = y_sun
Z_gc = z_sun
R_gc = np.sqrt(X_gc**2 + Y_gc**2)
phi_gc = np.arctan2(Y_gc, X_gc)

# Surface and volumetric density
sigma = sigma0 * np.exp(-R_gc / Rd)
rho = sigma / (2.0 * hz) * np.exp(-np.abs(Z_gc) / hz)

# ===== Arm membership (local phi grid search) =====
print(f"Evaluating arm membership...")
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

# ===== Results =====
V_shell = 4.0/3.0 * math.pi * (r2**3 - r1**3)
mean_rho = np.mean(rho)
N_expected_shell = mean_rho * V_shell
mean_rho_in_arms = np.mean(rho * in_arm)
N_expected_arms = mean_rho_in_arms * V_shell
frac_points_in_arm = np.mean(in_arm)

print(f"Shell radii: {r1_ly:.1f}..{r2_ly:.1f} ly -> {r1:.1f}..{r2:.1f} pc; N_mc={N_mc}")
print(f"Disk params: R0={R0_pc:.1f} pc, Rd={Rd:.1f} pc, hz={hz:.1f} pc, sigma0={sigma0:.3e} pc^-2")
print(f"Arms used: {len(arm_params)} (CSV loaded: {use_reid_csv})")
print('---')
print(f"Shell volume = {V_shell:.3e} pc^3")
print(f"Mean volumetric density in shell = {mean_rho:.3e} pc^-3")
print(f"Expected G stars in shell (all) = {N_expected_shell:.3f}")
print(f"Density-weighted expected in arms = {N_expected_arms:.3f}")
print(f"Geometric fraction of sampled points in arm region = {frac_points_in_arm:.5f}")

# Sensitivity sweep
for N_tot in [5e9, 1e10, 2e10, 5e10]:
    sigma0_loc = compute_sigma0(N_tot, Rd, Rmax)
    sigma_loc = sigma0_loc * np.exp(-R_gc / Rd)
    rho_loc = sigma_loc / (2.0 * hz) * np.exp(-np.abs(Z_gc) / hz)
    N_loc = np.mean(rho_loc * in_arm) * V_shell
    print(f"N_total_G={N_tot:.2e} -> Expected in arms ≈ {N_loc:.3e}")

# Save results to JSON
result = {
    "V_shell": float(V_shell),
    "N_expected_shell": float(N_expected_shell),
    "N_expected_arms": float(N_expected_arms),
    "frac_points_in_arm": float(frac_points_in_arm),
    "params": {
        "R0_pc": float(R0_pc),
        "Rd": float(Rd),
        "hz": float(hz),
        "arm_half_width": float(arm_half_width),
        "N_total_G": float(N_total_G),
        "N_mc": int(N_mc),
        "use_reid_csv": bool(use_reid_csv)
    }
}

output_file = 'g_star_results_1M.json'
with open(output_file, 'w') as f:
    json.dump(result, f, indent=2)

print(f"\nResults written to {output_file}")
print(json.dumps(result, indent=2))
