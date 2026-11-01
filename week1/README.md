# Week 1 Data Visualization Submission

## Student information

- **Name:** [Enter your full name]
- **Roll number:** [Enter your roll number]
- **Section:** [Enter your section]
- **Tasks attempted:** Tasks 1, 2, 3, 4, and 5

Replace the three bracketed fields above with your own details before submitting.

## Notebook files

| Notebook | Dataset | Main work |
|---|---|---|
| `task1.ipynb` | Datasaurus | Grouped summary statistics and a 13-panel scatter grid |
| `task2.ipynb` | Gapminder | Spaghetti plot, continent aggregation, selective highlighting, GDP gap, and skew |
| `task3.ipynb` | Penguins | Missing-data handling, body-mass distributions, Simpson's paradox, and species-sex means |
| `task4.ipynb` | MPG | Five question-matched charts and a redesigned weight/MPG plot |
| `task5.ipynb` | Flights | Monthly time series, seasonal views, report choice, and normalized seasonal index |

Every chart is followed by Markdown that states the finding, explains the chart choice, and discloses relevant exclusions or limitations.

## Run the notebooks

From the repository root, install the notebook dependencies:

```powershell
py -m pip install pandas numpy matplotlib jupyter ipykernel
```

Then open `week1/task1.ipynb` through `week1/task5.ipynb` in Jupyter or VS Code and run each notebook from top to bottom. The notebooks find the included CSVs using paths relative to the repository or the `week1` directory; they do not depend on a particular drive or username.

To rebuild the notebook source cells after editing the generator:

```powershell
py week1/create_week1_notebooks.py
```

Regenerate notebook outputs by rerunning each notebook after rebuilding.

## Data and scope

The five assignment CSV files are in `assignments/data/`. The supplied datasets are retained locally so the notebooks can run without downloading files. Instructor-provided task sheets and download scripts are not included in this student submission; assignment requirements are addressed in the notebook narratives.
