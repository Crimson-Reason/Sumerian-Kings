# Sumerian Kings — Star & Drake Analysis 🔭

A Monte Carlo analysis combining stellar population estimates and Drake-equation style probabilistic modeling to explore the likelihood of advanced civilizations within Earth-centered galactic shells.

---

## Table of contents

- [Project summary](#project-summary)
- [Key results](#key-results)
- [Prerequisites & installation](#prerequisites--installation)
- [Quick start](#quick-start)
- [Notebooks & scripts](#notebooks--scripts)
- [Data and outputs](#data-and-outputs)
- [Reproducibility tips](#reproducibility-tips)
- [Contributing & contact](#contributing--contact)

---

## Project summary

This repository contains notebooks and utilities to:
- Estimate O- and G-type star counts in distance shells around the Sun
- Model civilization detection probabilities using Drake-like parameters
- Incorporate spiral-arm geometry from published loci (e.g., Reid et al. 2014)

The analysis focuses on Earth-centered shells and produces probabilistic estimates with uncertainty quantified by Monte Carlo sampling.

## Key results ✅

- Example result from the analysis presented here: an expectation on the order of ~0.1 advanced civilizations in the analyzed shell under the chosen assumptions. This is model- and assumption-dependent — see the notebooks for details and parameter choices.

---

## Prerequisites & installation 🔧

Recommended: Windows PowerShell (instructions below), Python 3.10+ and a virtual environment.

1) Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Install dependencies from `requirements.txt` (preferred):

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

If you only need minimal packages for quick exploration, `numpy` and `jupyter` are the primary requirements.

---

## Quick start ▶️

Open the `Jupyter/` folder and launch Jupyter or open notebooks in VS Code:

```powershell
pip install jupyter
cd Jupyter
jupyter notebook
```

Recommended notebooks to start with:
- `Jupyter/o_star_spiral_model.ipynb` — O-star shell model and spiral-arm integration
- `Jupyter/g_star_spiral_model.ipynb` — G-star analysis
- `Jupyter/sumerian-kings-monte-carlo-model.ipynb` — Monte Carlo & sensitivity runs

You can run the main Monte Carlo cells interactively, or extract the core logic into a script for batch runs.

---

## Notebooks & scripts 🧩

- Notebooks: see the `Jupyter/` directory for interactive analysis and visualizations.
- Scripts: see the `Python/` directory for helper scripts (e.g., `create_reid_arms.py`, `create_session_summary_docx.py`, `merge_session_summaries.py`). Run them with:

```powershell
python Python\create_reid_arms.py
```

If you'd like, I can convert a notebook into a standalone Python script with a small CLI for reproducible runs.

---

## Data & outputs 📂

- Input data: `Data/` (contains `reid_arms.csv`, Sumerian king CSVs, and other inputs).
- Results: `Results/` (JSON, CSV, NPZ files and figures from runs).
- LaTeX files are in `Tex/` (can be compiled to PDF).

To use a published spiral-arm CSV (Reid+2014), place `reid_arms.csv` in the repository root (or `Data/`), with rows like:

```
name,R_ref_pc,phi_ref_deg,pitch_deg
```

No header is required by the scripts that load the file by default.

---

## Reproducibility tips 🧪

- To reproduce a Monte Carlo run exactly, set `np.random.seed(...)` near the top of the notebook before sampling.
- Increase the `N_mc` parameter to reduce Monte Carlo uncertainty (the published runs used ~250,000 samples).

---

## LaTeX / PDF

To compile the included LaTeX (`Tex/`), run (requires `pdflatex` installed):

```powershell
cd Tex
pdflatex -interaction=nonstopmode relavitistic-interpretation-of-sumerian-kings.tex
```

(Adjust file name as needed.)

---

## Contributing & contact 🤝

- Please open issues or submit pull requests for fixes and improvements.
- If you'd like: I can convert notebooks to reproducible scripts, add a small CLI, or generate a PDF with embedded figures from notebook outputs — tell me which and I can implement it.

---

**Notes:** This analysis depends strongly on parameter choices and stellar population assumptions. Interpret results as model-driven estimates rather than definitive counts.

---

*Updated*: README rewritten for clarity, setup, and reproducibility. If you want, I can also add a `LICENSE` file or a short CONTRIBUTING guide.