
from matplotlib.pyplot import plot
import pandas as pd
import numpy as np
from scipy.stats import truncnorm



kish_kings = [
      # Antediluvian (mythical) kings
    ("Jushur", 1200),
    ("Kullassina-bel", 960),
    ("Nangishlishma", 670),
    ("En-tarah-ana", 420),
    ("Babum", 300),
    ("Puannum", 840),
    ("Kalibum", 960),
    ("Zuqaqip", 900),
    ("Atab", 600),
    ("Mashda", 840),
    ("Arwium", 720),
    ("Etana", 1560),
    ("Balih", 400),
    ("En-men-lu-ana", 1200),
    ("Dumuzid, the Shepherd", 1000),
    ("Ensipazi-anna", 700),
    ("Enmengal-ana", 670),
    ("Dumuzid, the Fisherman", 1000),

    # Postdiluvian (legendary/early historical) kings
    ("En-me-barage-si", 900),
    ("Aga", 625)
]

# Useful derived structures
king_names = [name for name, years in kish_kings]
reigns = np.array([years for name, years in kish_kings], dtype=float)

N_samples = 10000
mu=45
sigma=15
lower_age = 10
upper_age = 80

a, b = (lower_age - mu) / sigma, (upper_age - mu) / sigma

y_samples = truncnorm.rvs(a, b, loc=mu, scale=sigma, size=N_samples)
a_samples_all = []
y_samples_all = []

# Monte Carlo sampling
for x_t in reigns:
    a_samples = np.random.uniform(0, 1, N_samples)
    y_samples = truncnorm.rvs(a, b, loc=mu, scale=sigma, size=N_samples)
    #y_samples = x_t * np.sqrt(1 - a_samples**2)
    valid = (y_samples >= 10) & (y_samples <= 80)
    a_samples_all.append(a_samples[valid])
    y_samples_all.append(y_samples[valid])

# Compute mean and percentiles
a_mean = np.array([np.mean(a) if len(a) > 0 else np.nan for a in a_samples_all])
a_lower = np.array([np.percentile(a, 5) if len(a) > 0 else np.nan for a in a_samples_all])
a_upper = np.array([np.percentile(a, 95) if len(a) > 0 else np.nan for a in a_samples_all])

y_mean = np.array([np.mean(y) if len(y) > 0 else np.nan for y in y_samples_all])
y_lower = np.array([np.percentile(y, 5) if len(y) > 0 else np.nan for y in y_samples_all])
y_upper = np.array([np.percentile(y, 95) if len(y) > 0 else np.nan for y in y_samples_all])

t = np.arange(len(reigns))

print(a_mean)
plot(t, a_mean)

