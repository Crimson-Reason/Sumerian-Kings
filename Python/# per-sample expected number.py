# per-sample expected number
weights = rho * (V_shell / N_mc)

# subsample for plotting
idx = np.random.choice(N_mc, size=plot_n, replace=False)
hb = ax.hexbin(x_sun[idx], y_sun[idx], C=weights[idx],
               reduce_C_function=np.sum, gridsize=200, cmap='viridis')
fig.colorbar(hb, ax=ax, label='Expected G stars per bin')