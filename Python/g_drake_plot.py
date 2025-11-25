#!/usr/bin/env python3
"""Run Drake Monte Carlo and produce distribution plots, saving samples.

Generates:
 - g_drake_samples.npz (samples: p, p_any, expected_n_civ)
 - per_star_p_hist.png
 - p_any_hist.png
 - expected_n_civ_hist.png
"""
import json
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--n-samples', '-N', type=int, default=100000)
parser.add_argument('--out-prefix', type=str, default='g_drake')
args = parser.parse_args()

n_samples = args.n_samples

# Load N_stars from g_star_results.json if present
import os
N_stars = None
if os.path.exists('g_star_results.json'):
    with open('g_star_results.json','r') as f:
        j = json.load(f)
    if 'N_expected_arms' in j:
        N_stars = float(j['N_expected_arms'])
    elif 'N_expected_shell' in j:
        N_stars = float(j['N_expected_shell'])
if N_stars is None:
    raise FileNotFoundError('g_star_results.json not found or missing expected counts')

N = N_stars

# constants and priors
t_star = 1.0e10
fp = 1.0
ne = 0.1

# log-uniform sampler
import random

def loguniform(low, high, size=None):
    return np.exp(np.random.uniform(math.log(low), math.log(high), size=size))

f_l = loguniform(1e-6, 1.0, size=n_samples)
f_i = loguniform(1e-6, 1.0, size=n_samples)
f_c = np.random.uniform(0.01,1.0,size=n_samples)
L = loguniform(1e2, 1e8, size=n_samples)

p = fp * ne * f_l * f_i * f_c * (L / t_star)
log1p_minus_p = np.log1p(-p)
exponent = N * log1p_minus_p
p_any = 1.0 - np.exp(exponent)
expected_n_civ = N * p

# save samples
np.savez_compressed(f'{args.out_prefix}_samples.npz', p=p, p_any=p_any, expected_n_civ=expected_n_civ, f_l=f_l, f_i=f_i, f_c=f_c, L=L)

# plots
plt.figure(figsize=(6,4))
plt.hist(p, bins=200, range=(0, np.quantile(p,0.999)), log=True)
plt.xlabel('Per-star p')
plt.ylabel('Counts (log)')
plt.title('Distribution of per-star p (truncated at 99.9%)')
plt.tight_layout()
plt.savefig(f'{args.out_prefix}_per_star_p_hist.png', dpi=200)
plt.close()

plt.figure(figsize=(6,4))
plt.hist(p_any, bins=200, range=(0, np.quantile(p_any,0.999)), log=True)
plt.xlabel('P(at least one)')
plt.ylabel('Counts (log)')
plt.title('Distribution of P(at least one) (truncated at 99.9%)')
plt.tight_layout()
plt.savefig(f'{args.out_prefix}_p_any_hist.png', dpi=200)
plt.close()

plt.figure(figsize=(6,4))
plt.hist(expected_n_civ, bins=200, range=(0, np.quantile(expected_n_civ,0.999)), log=True)
plt.xlabel('Expected number of civilizations (N * p)')
plt.ylabel('Counts (log)')
plt.title('Distribution of expected civilization counts (truncated at 99.9%)')
plt.tight_layout()
plt.savefig(f'{args.out_prefix}_expected_n_civ_hist.png', dpi=200)
plt.close()

print('Saved samples and plots with prefix', args.out_prefix)
