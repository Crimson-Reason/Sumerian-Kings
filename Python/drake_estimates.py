"""Compute Drake-style probabilities for a small set of stars.

This script defines three scenarios (optimistic, moderate, pessimistic)
and computes the per-star probability and the probability that at least
one of `n_stars` hosts an advanced society.

Run with: python drake_estimates.py
"""
import math
from typing import Dict


def drake_probability(fp, ne, fl, fi, fc, L, t_star):
    """Compute per-star probability p using simplified Drake-like factors."""
    return fp * ne * fl * fi * fc * (L / t_star)


def at_least_one(p, n):
    return 1.0 - (1.0 - p) ** n


def run_scenarios(n_stars=2) -> Dict[str, Dict[str, float]]:
    t_star = 1e10  # representative g-star lifetime in years

    scenarios = {
        "optimistic": dict(fp=1.0, ne=0.20, fl=1.0, fi=0.10, fc=0.50, L=1.0e6),
        "moderate": dict(fp=1.0, ne=0.10, fl=0.10, fi=0.01, fc=0.10, L=1.0e5),
        "pessimistic": dict(fp=0.5, ne=0.01, fl=1e-6, fi=1e-6, fc=0.1, L=1e4),
    }

    results = {}
    for name, params in scenarios.items():
        p = drake_probability(params['fp'], params['ne'], params['fl'], params['fi'], params['fc'], params['L'], t_star)
        p_any = at_least_one(p, n_stars)
        results[name] = {
            'per_star_p': p,
            'p_at_least_one': p_any,
            'n_stars': n_stars,
            'params': params,
            't_star': t_star,
        }
    return results


def print_results(results):
    for name, r in results.items():
        print(f"Scenario: {name}")
        print(f"  Per-star probability (p): {r['per_star_p']:.3e}")
        print(f"  Probability at least one of {r['n_stars']} stars has an advanced society: {r['p_at_least_one']:.3e}")
        print("  Parameters:")
        for k, v in r['params'].items():
            print(f"    {k} = {v}")
        print(f"    t_star = {r['t_star']:.3e} yr")
        print()


if __name__ == '__main__':
    res = run_scenarios(n_stars=2)
    print_results(res)
