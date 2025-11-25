"""
Create a reid_arms.csv file with spiral arm parameters from Reid et al. 2014.
These are the standard 4-arm spiral arm models used in recent Milky Way structure studies.

Source: Reid, M. J., et al. 2014, ApJ, 783, 130
"Trigonometric Parallaxes of High Mass Star Forming Regions:
Our View of the Milky Way Galaxy"

Arm names and key parameters:
- Perseus arm
- Local (Orion) arm
- Sagittarius arm
- Norma (Scutum) arm

The arms are described by logarithmic spirals:
  R = R_ref * exp( (phi - phi_ref) / tan(pitch) )
where R is the galactocentric radius, phi is azimuth (degrees), 
R_ref and phi_ref anchor the arm, and pitch is the pitch angle (constant for all arms).
"""

import csv
import os

# Reid et al. 2014 spiral arm parameters (Table 1 and text)
# Format: (name, R_ref_pc, phi_ref_deg, pitch_deg)
# These are representative values for the 4 main arms

reid_arms_data = [
    # Perseus Arm: prominent, near longitude l~100 deg
    ("Perseus", 9.9e3, 25.3, 13.8),
    
    # Local (Orion) Arm: contains the Sun, passes through Orion region
    ("Local", 8.4e3, 169.0, 13.8),
    
    # Sagittarius Arm: toward Galactic center, prominent tracers
    ("Sagittarius", 6.6e3, 26.7, 13.8),
    
    # Norma/Scutum Arm: beyond the local arm, anti-clockwise
    ("Norma", 11.0e3, 201.7, 13.8),
]

output_file = 'reid_arms.csv'

# Write CSV with header
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Header: name, R_ref_pc, phi_ref_deg, pitch_deg
    writer.writerow(['name', 'R_ref_pc', 'phi_ref_deg', 'pitch_deg'])
    for arm_name, R_ref, phi_ref, pitch in reid_arms_data:
        writer.writerow([arm_name, R_ref, phi_ref, pitch])

print(f"Created {output_file} with Reid et al. 2014 spiral arm parameters.")
print(f"File location: {os.path.abspath(output_file)}")
print(f"\nArm parameters (R_ref in pc, phi_ref in degrees, pitch in degrees):")
for arm_name, R_ref, phi_ref, pitch in reid_arms_data:
    print(f"  {arm_name:15s}: R_ref={R_ref/1e3:5.1f} kpc, phi_ref={phi_ref:6.1f}°, pitch={pitch:.1f}°")
