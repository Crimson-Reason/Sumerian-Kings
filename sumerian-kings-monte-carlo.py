
from matplotlib.pyplot import plot
import pandas as pd
import numpy as np
from scipy.stats import truncnorm



kish_kings = [
    ("Jushur", 1200),
    ("Kullassina-bel", 960),
    ("Nangishlishma", 670),
    ("En-tarah-ana", 420),
    ("Babum", 300),
    ("Puannum", 840),
    ("Kalibum", 960),
    ("Kalumum", 840),
    ("Zuqaqip", 900),
    ("Atab (Aba)", 600),
    ("Mashda", 840),
    ("Arwium", 720),
    ("Etana", 1500),
    ("Balih", 400),
    ("En-me-nuna", 660),
    ("Melem-Kish", 900),
    ("Barsal-nuna", 1200),
    ("Zamug", 140),
    ("Tizqar", 305),
    ("Ilku", 900),
    ("Iltasadum", 1200),
    ("Enmebaragesi", 900),
    ("Aga of Kish", 625),
    ("Susuda", 201),
    ("Dadasig", 81),
    ("Mamagal", 360),
    ("Kalbum", 195),
    ("Tuge", 360),
    ("Men-nuna", 180),
    ("Enbi-Ištar", 290),
    ("Lugalngu", 360),
    ("Kug-Bau (female)", 100),
    ("Puzur-Suen", 25),
    ("Ur-Zababa", 400),
    ("Zimudar", 30),
    ("Usi-watar", 7),
    ("Eshtar-muti", 11),
    ("Ishme-Shamash", 11),
    ("Nanniya", 7),
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

