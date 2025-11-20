import numpy as np
import matplotlib.pyplot as plt

# Example reigns in years (Sumerian King List - pre-flood)
king_names = [
"Jushur",
"Kullassina-bel",
"Nangishlishma",
"En-tarah-ana",
"Babum",
"Puannum",
"Kalibum",
"Kalumum",
"Zuqaqip",
"Atab (Aba)",
"Mashda",
"Arwium",
"Etana",
"Balih",
"En-me-nuna",
"Melem-Kish",
"Barsal-nuna",
"Zamug",
"Tizqar",
"Ilku",
"Iltasadum",
"Enmebaragesi",
"Aga of Kish",
"Susuda",
"Dadasig",
"Mamagal",
"Kalbum",
"Tuge",
"Men-nuna",
"Enbi-Ištar",
"Lugalngu",
"Kug-Bau (female)",
"Puzur-Suen",
"Ur-Zababa",
"Zimudar",
"Usi-watar",
"Eshtar-muti",
"Ishme-Shamash",
"Nanniya"
]

reigns = np.array([
 1200 ,
 960 ,
 670 ,
 420 ,
 300 ,
 840 ,
 960 ,
 840 ,
 900 ,
 600 ,
 840 ,
 720 ,
 1500 ,
 400 ,
 660 ,
 900 ,
 1200 ,
 140 ,
 305 ,
 900 ,
 1200 ,
 900 , 
 625 ,
 201 ,
 81 ,
 360 ,
 195 ,
 360 ,
 180 ,
 290 ,
 360 ,
 100 , 
 25 ,
 400 ,
 30 ,
 7 ,
 11 ,
 11 ,
 7 ])  # in Earth years

# Assumed proper lifetime (experienced by the king)
t0 = 40  # years of an average reign - free parameter of the model

# Speed of light (normalized to 1 if using units of c)
c = 1

#debugging code
ratios = t0 / reigns
#print("t0/reigns values:")
#for name, ratio in zip(king_names, ratios):
#    print(f"{name}: {ratio:.4f}")

new_ratios = np.where(ratios <= 1, ratios, 0.9999995)
#print("\nAdjusted new_ratios values:", new_ratios)
# Solve for v for each king, with special handling if t0 > reign
velocities = c * np.sqrt(1 - (new_ratios) ** 2)



# Plot
plt.figure(figsize=(10, 5))
plt.plot(king_names, velocities, color='steelblue')
plt.ylabel('Inferred Velocity (as fraction of c)')
plt.title(f'Inferred Speeds of Sumerian Kings (Assuming $t_0$ = {t0} years)')
#plt.yscale('log')  # Set Y-axis to logarithmic scale
plt.ylim(0.00, 1.001)
plt.xticks(rotation=45)
plt.grid(True, axis='y')
plt.tight_layout()
plt.show()

# Calculate distance for each king (in light-years)
distances = velocities * reigns  # since c=1, units are light-years

# (Optional) Print each king's distance
print("\nKing-by-king distances:")
for name, reign, v, d in zip(king_names, reigns, velocities, distances):
    print(f"{name:<20} {reign:>6} yrs  v={v:6.4f}c  distance={d:8.2f} ly")

# Total distance traveled (sum of all reigns at their respective speeds)
total_distance = np.sum(distances)

print(f"Total distance traveled during the voyage: {total_distance:.2f} light-years")

# Estimate net displacement from Earth after random walk
step_sizes = distances  # already velocities * reigns
expected_distance = np.sqrt(np.sum(step_sizes ** 2))
print(f"Estimated net displacement from Earth after random walk: {expected_distance:.2f} light-years")


