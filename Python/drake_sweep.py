"""Sweep key Drake parameters and write results to CSV.

This script sweeps over fl and fi (probabilities of life and intelligence)
and writes per-star and at-least-one probabilities for n_stars=2.

Run with: python drake_sweep.py
"""
import csv
import math

# fixed values
t_star =1e10 # representative g-star lifetime in years
#t_star = 5.0e6
fp = 1.0
ne = 0.1
fc = 0.1
L = 1.0e5
n_stars = 2

# ranges to sweep (log-spaced for very small probabilities)
fl_values = [1.0, 1e-1, 1e-2, 1e-3, 1e-4, 1e-6]
fi_values = [1e-0, 1e-1, 1e-2, 1e-3, 1e-6]

out_path = 'drake_sweep_results.csv'
with open(out_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['fl', 'fi', 'per_star_p', 'p_at_least_one'])
    for fl in fl_values:
        for fi in fi_values:
            p = fp * ne * fl * fi * fc * (L / t_star)
            p_any = 1.0 - (1.0 - p) ** n_stars
            writer.writerow([fl, fi, f"{p:.12e}", f"{p_any:.12e}"])

print(f"Wrote sweep results to {out_path}")
