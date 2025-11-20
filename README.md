# Reproduce O-star Monte Carlo and TeX build

This folder contains:
- `o_star_spiral_model.ipynb` — Monte Carlo notebook estimating O-type star counts in a spherical shell. Supports using a `reid_arms.csv` spiral-arm locus if present; otherwise falls back to a parametric 4-arm model.
- `o_star_calculations.tex` — LaTeX write-up with analytic calculations and the Monte Carlo outputs.
- `o_star_calculations.pdf` — Compiled PDF (if present).

Requirements
- Python 3.8+ with `numpy` installed for the notebook (the notebook uses only NumPy and Python standard library).
- Jupyter or VS Code with Jupyter support to open and run the notebook interactively.
- A LaTeX distribution (e.g., MiKTeX on Windows) to compile the `.tex` file to PDF.

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