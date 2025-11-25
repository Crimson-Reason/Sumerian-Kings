"""
G-Drake Sweep execution script - generates results and visualization.
Run with: python g_drake_sweep_execute.py
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Fixed Drake Parameters
t_star = 5.0e6
fp = 1.0
ne = 0.1
fc = 0.1
L = 1.0e5
n_stars = 2

# Sweep Ranges
fl_values = [1.0, 1e-1, 1e-2, 1e-3, 1e-4, 1e-6]
fi_values = [1e-0, 1e-1, 1e-2, 1e-3, 1e-6]

# Perform Sweep
results = []
for fl in fl_values:
    for fi in fi_values:
        p = fp * ne * fl * fi * fc * (L / t_star)
        p_any = 1.0 - (1.0 - p) ** n_stars
        results.append({'fl': fl, 'fi': fi, 'per_star_p': p, 'p_at_least_one': p_any})

df = pd.DataFrame(results)

# Export to CSV
output_file = 'g_drake_sweep_results.csv'
df.to_csv(output_file, index=False, float_format='%.12e')

print(f"✓ Exported sweep results to: {output_file}")
print(f"\nSweep Summary:")
print(f"  Per-star p range: {df['per_star_p'].min():.3e} to {df['per_star_p'].max():.3e}")
print(f"  P(at least one) range: {df['p_at_least_one'].min():.3e} to {df['p_at_least_one'].max():.3e}")
print(f"\nOptimistic (fl=1, fi=1): p={df[(df['fl']==1.0) & (df['fi']==1.0)]['per_star_p'].values[0]:.3e}, P_any={df[(df['fl']==1.0) & (df['fi']==1.0)]['p_at_least_one'].values[0]:.3e}")
print(f"Pessimistic (fl=1e-6, fi=1e-6): p={df[(df['fl']==1e-6) & (df['fi']==1e-6)]['per_star_p'].values[0]:.3e}, P_any={df[(df['fl']==1e-6) & (df['fi']==1e-6)]['p_at_least_one'].values[0]:.3e}")

# Create heatmap visualization
pivot_per_star = df.pivot_table(values='per_star_p', index='fi', columns='fl').sort_index(ascending=False)
pivot_p_any = df.pivot_table(values='p_at_least_one', index='fi', columns='fl').sort_index(ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

im1 = axes[0].imshow(np.log10(pivot_per_star.values), cmap='YlOrRd', aspect='auto')
axes[0].set_xlabel('$f_l$ (log scale)', fontsize=11)
axes[0].set_ylabel('$f_i$ (log scale)', fontsize=11)
axes[0].set_title('Per-Star Probability $p$ (log-scale)', fontsize=12)
axes[0].set_xticks(range(len(pivot_per_star.columns)))
axes[0].set_xticklabels([f'{x:.0e}' for x in pivot_per_star.columns], rotation=45, ha='right')
axes[0].set_yticks(range(len(pivot_per_star.index)))
axes[0].set_yticklabels([f'{x:.0e}' for x in pivot_per_star.index])
cbar1 = plt.colorbar(im1, ax=axes[0])
cbar1.set_label('log₁₀(p)', fontsize=10)

im2 = axes[1].imshow(np.log10(pivot_p_any.values + 1e-20), cmap='Blues', aspect='auto')
axes[1].set_xlabel('$f_l$ (log scale)', fontsize=11)
axes[1].set_ylabel('$f_i$ (log scale)', fontsize=11)
axes[1].set_title(f'P(At Least One | n=2) (log-scale)', fontsize=12)
axes[1].set_xticks(range(len(pivot_p_any.columns)))
axes[1].set_xticklabels([f'{x:.0e}' for x in pivot_p_any.columns], rotation=45, ha='right')
axes[1].set_yticks(range(len(pivot_p_any.index)))
axes[1].set_yticklabels([f'{x:.0e}' for x in pivot_p_any.index])
cbar2 = plt.colorbar(im2, ax=axes[1])
cbar2.set_label('log₁₀(P)', fontsize=10)

plt.tight_layout()
plt.savefig('g_drake_sweep_heatmap.png', dpi=150, bbox_inches='tight')
print(f"✓ Heatmap saved to: g_drake_sweep_heatmap.png")
