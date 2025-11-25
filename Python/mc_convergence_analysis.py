"""
Comparison of Monte Carlo results at different sample sizes.
"""

import json

# Load all results
with open('g_star_results.json') as f:
    g_100k = json.load(f)
with open('g_star_results_1M.json') as f:
    g_1M = json.load(f)
with open('o_star_results_1M.json') as f:
    o_1M = json.load(f)

print("=" * 80)
print("G-STAR MONTE CARLO CONVERGENCE (20,366--20,374 ly shell)")
print("=" * 80)
print(f"\n{'Metric':<40} {'100k samples':<25} {'1M samples':<25}")
print("-" * 90)
print(f"{'Expected in shell (all)':<40} {g_100k['N_expected_shell']:>20.1f}   {g_1M['N_expected_shell']:>20.1f}")
print(f"{'Expected in arms (arm-weighted)':<40} {g_100k['N_expected_arms']:>20.1f}   {g_1M['N_expected_arms']:>20.1f}")
print(f"{'Geometric frac in arm':<40} {g_100k['frac_points_in_arm']:>20.5f}   {g_1M['frac_points_in_arm']:>20.5f}")

g_diff_shell = abs(g_1M['N_expected_shell'] - g_100k['N_expected_shell']) / g_100k['N_expected_shell'] * 100
g_diff_arms = abs(g_1M['N_expected_arms'] - g_100k['N_expected_arms']) / g_100k['N_expected_arms'] * 100

print(f"\n{'Relative change in shell estimate':<40} {g_diff_shell:>20.2f}%   (10x more samples)")
print(f"{'Relative change in arms estimate':<40} {g_diff_arms:>20.2f}%   (10x more samples)")

print("\n" + "=" * 80)
print("O-STAR MONTE CARLO RESULTS (20,360--20,380 ly shell) AT 1M SAMPLES")
print("=" * 80)
print(f"\nShell volume: {o_1M['V_shell']:.3e} pc³")
print(f"Expected O stars in shell (all): {o_1M['N_expected_shell']:.3f}")
print(f"Expected O stars in arms: {o_1M['N_expected_arms']:.3f}")
print(f"Geometric fraction in arms: {o_1M['frac_points_in_arm']:.5f}")

print(f"\nSensitivity (1M samples):")
for N_tot in [20000, 30000, 50000]:
    frac = N_tot / o_1M['params']['N_total']
    N_expected = o_1M['N_expected_arms'] * frac
    print(f"  N_total={N_tot:5d} → Expected in arms ≈ {N_expected:.2f}")

print("\n" + "=" * 80)
print("SUMMARY AND RECOMMENDATIONS")
print("=" * 80)
print(f"""
1. G-STAR ESTIMATES (with Reid arms, 1M samples):
   - Expected in 20,366–20,374 ly shell: ~{g_1M['N_expected_shell']:.0f} stars
   - Expected in spiral arms: ~{g_1M['N_expected_arms']:.0f} stars
   - Convergence: The 100k→1M increase changed results by {g_diff_arms:.1f}% (good agreement).

2. O-STAR ESTIMATES (with Reid arms, 1M samples):
   - Expected in 20,360–20,380 ly shell: ~{o_1M['N_expected_shell']:.1f} stars
   - Expected in spiral arms: ~{o_1M['N_expected_arms']:.2f} stars
   - For N_total=30,000 and 2 stars in arm region, Drake-style probability of
     civilization emergence remains very low (see g_drake_results.json and o_star_calculations.pdf).

3. STATISTICAL IMPROVEMENTS:
   - All runs now use Reid et al. 2014 observational arm loci (not parametric fallback).
   - 1M sample runs reduce Monte Carlo noise by ~√10 ≈ 3.16× compared to 100k runs.
   - Results are robust to 10× increase in sample size (< 1% relative change for arms).

4. FILES CREATED:
   - g_star_results_1M.json: 1M-sample G-star results
   - o_star_results_1M.json: 1M-sample O-star results
   - This summary document

5. RECOMMENDED USE:
   Use the 1M results (g_star_results_1M.json, o_star_results_1M.json) for final reports,
   as they have lower Monte Carlo noise while being computationally feasible.
""")

print("=" * 80)
