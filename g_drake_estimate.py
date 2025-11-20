#!/usr/bin/env python3
"""Monte Carlo Drake Equation estimate for G-type stars.

Reads `g_star_results.json` for the estimated number of G-type stars in the
shell (or accepts an override), samples priors for key Drake factors, and
computes distributions for the per-star probability and the probability that
at least one of the stars currently hosts a technological civilization.

Output: prints summary to stdout and writes `g_drake_results.json`.
"""
import json
import math
import argparse
import numpy as np
import os


def loguniform(low, high, size=None):
    return np.exp(np.random.uniform(math.log(low), math.log(high), size=size))


def main():
    parser = argparse.ArgumentParser(description='G-type Drake Equation Monte Carlo')
    parser.add_argument('--n-samples', '-N', type=int, default=100000,
                        help='Monte Carlo samples (default: 100000)')
    parser.add_argument('--n-stars', type=float, default=None,
                        help='Number of G-type stars to use (overrides JSON)')
    parser.add_argument('--json', type=str, default='g_star_results.json',
                        help='Path to g_star_results.json')
    parser.add_argument('--out', type=str, default='g_drake_results.json',
                        help='Output JSON file')
    args = parser.parse_args()

    # Load N_stars estimate from JSON if available
    N_stars = None
    if args.n_stars is not None:
        N_stars = float(args.n_stars)
    else:
        if os.path.exists(args.json):
            with open(args.json, 'r') as f:
                j = json.load(f)
            # use density-weighted expected in arms if present, else total expected
            if 'N_expected_arms' in j:
                N_stars = float(j['N_expected_arms'])
            elif 'N_expected_shell' in j:
                N_stars = float(j['N_expected_shell'])
    if N_stars is None:
        raise FileNotFoundError(f"No JSON found at {args.json} and --n-stars not provided")

    N = N_stars

    # Fixed / assumed constants
    t_star = 1.0e10  # G-type main-sequence lifetime in years (~10 Gyr)
    fp = 1.0         # fraction of stars with planets (optimistic)
    ne = 0.1         # number of potentially habitable planets per star (order-of-magnitude)

    n_samples = int(args.n_samples)

    # Priors for uncertain parameters (these choices are adjustable):
    # f_l: fraction of habitable planets that develop life: log-uniform [1e-6, 1.0]
    # f_i: fraction of life-bearing planets that develop intelligence: log-uniform [1e-6, 1.0]
    # f_c: fraction of intelligent species that become communicative/technological: uniform [0.01, 1]
    # L: lifetime of a technological civilization in years: log-uniform [1e2, 1e8]

    rng = np.random.default_rng()

    f_l = loguniform(1e-6, 1.0, size=n_samples)
    f_i = loguniform(1e-6, 1.0, size=n_samples)
    f_c = rng.uniform(0.01, 1.0, size=n_samples)
    L = loguniform(1e2, 1e8, size=n_samples)

    # Per-sample per-star probability p
    p = fp * ne * f_l * f_i * f_c * (L / t_star)

    # Handle extreme small/large values properly and compute p_any = 1 - (1-p)^N
    # Use stable computation: p_any = 1 - exp(N * log1p(-p))
    log1p_minus_p = np.log1p(-p)
    exponent = N * log1p_minus_p
    # Avoid exponent underflow: where N*p is tiny, approximate p_any ~ 1 - exp(-N*p)
    # but np.exp on large negative is fine; just compute safely
    p_any = 1.0 - np.exp(exponent)

    # Expected number of civilizations (mean across samples)
    expected_n_civ = N * p

    # Summaries
    def q(x):
        return np.quantile(x, [0.001, 0.01, 0.05, 0.16, 0.5, 0.84, 0.95, 0.99, 0.999])

    summary = {
        'N_stars_used': N,
        'n_samples': n_samples,
        'per_star_p_quantiles': q(p).tolist(),
        'per_star_p_mean': float(np.mean(p)),
        'per_star_p_median': float(np.median(p)),
        'p_any_quantiles': q(p_any).tolist(),
        'p_any_mean': float(np.mean(p_any)),
        'p_any_median': float(np.median(p_any)),
        'expected_n_civ_quantiles': q(expected_n_civ).tolist(),
        'expected_n_civ_mean': float(np.mean(expected_n_civ)),
        'expected_n_civ_median': float(np.median(expected_n_civ)),
        'priors': {
            'fp': fp,
            'ne': ne,
            'f_l_range': [1e-6, 1.0],
            'f_i_range': [1e-6, 1.0],
            'f_c_range': [0.01, 1.0],
            'L_range_years': [1e2, 1e8],
            't_star_years': t_star
        }
    }

    # Save results
    with open(args.out, 'w') as f:
        json.dump(summary, f, indent=2)

    # Print concise human-readable summary
    print(f"G-type Drake Monte Carlo: N_stars = {N:.3g}, n_samples = {n_samples}")
    print(f"Per-star p (median) = {summary['per_star_p_median']:.3e}, mean = {summary['per_star_p_mean']:.3e}")
    print(f"P(at least one) median = {summary['p_any_median']:.3e}, mean = {summary['p_any_mean']:.3e}")
    print(f"Expected civilizations (median) = {summary['expected_n_civ_median']:.3e}, mean = {summary['expected_n_civ_mean']:.3e}")
    print(f"Results written to {args.out}")


if __name__ == '__main__':
    main()
