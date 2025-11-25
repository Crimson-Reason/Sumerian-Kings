import numpy as np
import math
import os
import json

# --- Shell in light years (Earth-centered) ---
r1_ly = 16408.70211 #lower radius in light-years
r2_ly = 16428.70211 #upper radius in light-years
ly_to_pc = 0.306601
r1 = r1_ly * ly_to_pc  # pc
r2 = r2_ly * ly_to_pc  # pc

# --- Galactic / stellar population parameters for G-type stars ---
R0_pc = 8122.0         # Sun galactocentric radius in pc (8.122 kpc)
Rd = 2600.0            # radial scale length for G stars (pc) - adjustable
hz = 300.0             # vertical scale height for G stars (pc) - adjustable
Rmax = 15000.0         # radial limit for normalization (pc)

# Spiral arms: try to load reid_arms.csv (name,R_ref_pc,phi_ref_deg,pitch_deg), else fallback to 4-arm model
use_reid_csv = os.path.exists('reid_arms.csv')
n_arms = 4
pitch_deg = 12.0
arm_half_width = 300.0  # pc, adjust for narrower/wider arms

# Population: total number of G-type stars in galaxy (adjustable). Default chosen as 2e10
N_total_G = 2.0e10

# Monte Carlo samples (adjust to trade speed/precision)
N_mc = 100000

# helper to normalize surface density to total N within Rmax
def compute_sigma0(N_total, Rd, Rmax):
    integral = 2 * math.pi * Rd**2 * (1 - math.exp(-Rmax/Rd)*(1 + Rmax/Rd))
    return N_total / integral

sigma0 = compute_sigma0(N_total_G, Rd, Rmax)

# load arms if CSV available
arm_params = []
if use_reid_csv:
    try:
        import csv
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
phi_gc = np.arctan2(Y_gc, X_gc)  # -pi..pi

# surface density at R (pc^-2)
sigma = sigma0 * np.exp(-R_gc / Rd)
# volumetric density using exponential vertical distribution: rho = sigma/(2*hz) * exp(-|z|/hz)
rho = sigma / (2.0 * hz) * np.exp(-np.abs(Z_gc) / hz)

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
    # phi_grid shape (N_mc, n_phi_samples)
    phi_grid = (phi_gc[:, None] + phi_offsets[None, :])
    phi_rel = (phi_grid - phi_ref + math.pi) % (2.0*math.pi) - math.pi
    R_arm_grid = R_ref * np.exp(phi_rel * tan_p)
    radial_sep_grid = np.abs(R_gc[:, None] - R_arm_grid)
    sep_min = np.minimum(sep_min, np.min(radial_sep_grid, axis=1))

in_arm = sep_min < arm_half_width

# compute full spherical shell volume
V_shell = 4.0/3.0 * math.pi * (r2**3 - r1**3)

# expected numbers
mean_rho = np.mean(rho)
N_expected_shell = mean_rho * V_shell
mean_rho_in_arms = np.mean(rho * in_arm)
N_expected_arms = mean_rho_in_arms * V_shell

# geometric arm fraction
frac_points_in_arm = float(np.mean(in_arm))

# print diagnostics and sensitivity over N_total_G
print(f"Shell radii: {r1_ly}..{r2_ly} ly -> {r1:.1f}..{r2:.1f} pc; N_mc={N_mc}")
print(f"Disk params: R0={R0_pc} pc, Rd={Rd} pc, hz={hz} pc, sigma0={sigma0:.3e} pc^-2")
print(f"Arms used: {len(arm_params)} (CSV loaded: {use_reid_csv})")
print('---')
print(f"Shell volume = {V_shell:.3e} pc^3")
print(f"Mean volumetric density in shell = {mean_rho:.3e} pc^-3")
print(f"Expected G stars in shell (all) = {N_expected_shell:.3f}")
print(f"Density-weighted expected in arms = {N_expected_arms:.3f}")
print(f"Geometric fraction of sampled points in arm region = {frac_points_in_arm:.6f}")

for Ntot in [5e9, 1e10, 2e10, 5e10]:
    sigma0_loc = compute_sigma0(Ntot, Rd, Rmax)
    sigma_loc = sigma0_loc * np.exp(-R_gc / Rd)
    rho_loc = sigma_loc / (2.0 * hz) * np.exp(-np.abs(Z_gc) / hz)
    Nloc = float(np.mean(rho_loc * in_arm) * V_shell)
    print(f"N_total_G={Ntot:.2e} -> Expected in arms ≈ {Nloc:.3f}")

result = dict(V_shell=V_shell, N_expected_shell=float(N_expected_shell), N_expected_arms=float(N_expected_arms), frac_points_in_arm=frac_points_in_arm, params=dict(R0_pc=R0_pc, Rd=Rd, hz=hz, arm_half_width=arm_half_width, N_total_G=N_total_G, N_mc=N_mc))

# write results to JSON
with open('g_star_results.json', 'w') as f:
    json.dump(result, f, indent=2)

print('\nResults written to g_star_results.json')
print(json.dumps(result, indent=2))
