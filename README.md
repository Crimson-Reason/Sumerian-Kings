# Sumerian-Kings: Star Analysis Project

A comprehensive Monte Carlo analysis of stellar populations and Drake equation probabilities, exploring the potential for advanced civilizations in Earth-centered galactic shells.

## Project Overview

This project estimates the number of O-type and G-type stars within specific distance shells from Earth, applies the Drake equation to compute civilization detection probabilities, and integrates observational spiral arm data from Reid et al. (2014).

**Key Finding:** Expected ~0.1 advanced civilizations in the analyzed shell, highlighting the Fermi Paradox.

Quick steps (PowerShell)

1) Create & activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Install requirements (NumPy):

```powershell
pip install --upgrade pip
pip install numpy
```

3) Run the notebook in Jupyter (interactive):

```powershell
pip install jupyter
jupyter notebook o_star_spiral_model.ipynb
```

or open `o_star_spiral_model.ipynb` in VS Code and run the main code cell.

4) If you prefer to run the Monte Carlo cell non-interactively you can extract its logic into a Python script and run it. The notebook's main cell is self-contained and uses only NumPy and math.

5) Compile the LaTeX file to PDF (requires `pdflatex` available in PATH):

```powershell
cd 'c:\Users\babak\Desktop\Innovation\Sumerian Kings'
pdflatex -interaction=nonstopmode o_star_calculations.tex
```

If `pdflatex` is not installed, install MiKTeX (Windows) or TeX Live (Linux/macOS) and re-run the command above.

Notes & tips
- To use a published spiral-arm locus (e.g., Reid+2014) place a CSV named `reid_arms.csv` in this folder with rows: `name,R_ref_pc,phi_ref_deg,pitch_deg` (no header). The notebook will automatically load it when present.
- If you want reproducible Monte Carlo runs, set `np.random.seed(...)` at the top of the notebook before sampling.
- For tighter Monte Carlo uncertainty, increase the `N_mc` parameter in the notebook (it was run here with 250,000 for the final results).

Contact
- If you'd like, I can (a) convert the notebook into a runnable Python script and provide a small CLI, or (b) produce a PDF with figures embedded from the notebook outputs. Let me know which you prefer.