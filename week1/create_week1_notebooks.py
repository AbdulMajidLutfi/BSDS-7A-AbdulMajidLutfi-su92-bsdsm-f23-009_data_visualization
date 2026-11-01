from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_SETUP = """from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def assignment_data(filename):
    candidates = (
        Path.cwd() / "week1" / "assignments" / "data" / filename,
        Path.cwd() / "assignments" / "data" / filename,
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    searched = "\\n".join(str(path) for path in candidates)
    raise FileNotFoundError(f"Could not find {filename}. Searched:\\n{searched}")
"""


def markdown(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(True)}


def code(text: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": text.splitlines(True),
    }


def notebook(title: str, cells: list[tuple[str, str]]) -> dict:
    notebook_cells = [markdown(
        f"# {title}\n\n"
        "Each chart is followed by a written interpretation. "
        "The notebook uses paths relative to the repository, not a machine-specific drive."
    )]
    notebook_cells[0]["id"] = "intro"
    for index, (kind, value) in enumerate(cells, start=1):
        cell = markdown(value) if kind == "markdown" else code(value)
        cell["id"] = f"cell-{index:03d}"
        notebook_cells.append(cell)
    return {
        "cells": notebook_cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def task1() -> dict:
    return notebook(
        "Week 1 · Task 1 — Prove why we visualize",
        [
            ("code", DATA_SETUP + """
df = pd.read_csv(assignment_data("datasaurus.csv"))
assert df["dataset"].nunique() == 13

summary_rows = []
for name, group in df.groupby("dataset", sort=True):
    summary_rows.append(
        {
            "dataset": name,
            "points": len(group),
            "x_mean": group["x"].mean(),
            "y_mean": group["y"].mean(),
            "x_sd": group["x"].std(ddof=1),
            "y_sd": group["y"].std(ddof=1),
            "correlation": group["x"].corr(group["y"]),
        }
    )
summary = pd.DataFrame(summary_rows).set_index("dataset")
summary.round(3)
"""),
            ("markdown", """### What the summary table says

The 13 datasets have nearly the same means, standard deviations, and x-y correlation. If these statistics were all we had, we might conclude that the datasets have essentially the same numerical structure. Each contains 142 points, so the similarity is not caused by a tiny sample.
"""),
            ("code", """
fig, axes = plt.subplots(4, 4, figsize=(15, 11), constrained_layout=True)
for ax, (name, group) in zip(axes.flat, df.groupby("dataset", sort=True)):
    ax.scatter(group["x"], group["y"], s=10, color="#176B87", alpha=0.82)
    ax.set_title(name)
    ax.set_aspect("equal", adjustable="datalim")
    ax.grid(alpha=0.15)
for ax in axes.flat[df["dataset"].nunique():]:
    ax.set_visible(False)
fig.suptitle("Nearly identical summaries conceal 13 different point patterns", fontsize=16)
plt.show()
"""),
            ("markdown", """### What the scatter grid reveals — and the answer

The point patterns are visibly different: some form curves, clusters, lines, or distinctive shapes. Similar averages and correlations do not imply similar distributions or relationships.

Having 13 datasets and 142 observations per dataset makes the calculated statistics more stable for each dataset, but it does **not** make those statistics a trustworthy substitute for inspecting the data. A larger sample can estimate the same limited summaries precisely while still hiding structure those summaries do not measure. The table and scatter grid answer different questions; both are needed.
"""),
        ],
    )


def task2() -> dict:
    return notebook(
        "Week 1 · Task 2 — Trends and the spaghetti problem",
        [
            ("code", DATA_SETUP + """
df = pd.read_csv(assignment_data("gapminder.csv")).sort_values(["country", "year"])
assert df["country"].nunique() == 142
"""),
            ("code", """
fig, ax = plt.subplots(figsize=(15, 8))
for country, group in df.groupby("country", sort=True):
    ax.plot(group["year"], group["lifeExp"], linewidth=0.8, alpha=0.35, label=country)
ax.set_title("Life expectancy rose across most countries, but 142 lines overwhelm detail")
ax.set_xlabel("Year")
ax.set_ylabel("Life expectancy (years)")
ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", ncol=3, fontsize=5, frameon=False)
ax.grid(axis="y", alpha=0.2)
plt.show()
"""),
            ("markdown", """### Why the all-country chart is deliberately messy

The lines show country-level variation, but 142 similarly styled trajectories overlap and the large legend is difficult to scan. The broad upward pattern is visible; tracing a particular country's path is not. This is the intended spaghetti-chart diagnosis, not a recommended final chart.
"""),
            ("code", """
continent = df.groupby(["continent", "year"], as_index=False)["lifeExp"].mean()
fig, ax = plt.subplots(figsize=(12, 6))
for name, group in continent.groupby("continent", sort=True):
    ax.plot(group["year"], group["lifeExp"], marker="o", linewidth=2.4, label=name)
ax.set_title("Average life expectancy increased in every continent")
ax.set_xlabel("Year")
ax.set_ylabel("Mean life expectancy (years)")
ax.legend(title="Continent", frameon=False, ncol=3)
ax.grid(axis="y", alpha=0.2)
plt.show()
"""),
            ("markdown", """### Fix A — aggregate by continent

Aggregation makes the broad regional trend readable and reduces 142 lines to five. It answers how continent averages changed, but hides differences among countries within each continent.
"""),
            ("code", """
highlight = {
    "Afghanistan": "#D1495B",
    "Japan": "#0F766E",
    "United States": "#2563EB",
}
fig, ax = plt.subplots(figsize=(12, 6))
for country, group in df.groupby("country", sort=True):
    if country in highlight:
        ax.plot(group["year"], group["lifeExp"], color=highlight[country], linewidth=2.5)
        last = group.iloc[-1]
        ax.annotate(
            country,
            (last["year"], last["lifeExp"]),
            xytext=(5, 0),
            textcoords="offset points",
            color=highlight[country],
            va="center",
        )
    else:
        ax.plot(group["year"], group["lifeExp"], color="#CBD5E1", linewidth=0.8, alpha=0.7)
ax.set_xlim(df["year"].min(), df["year"].max() + 8)
ax.set_title("Three country trajectories stand out against the other 139")
ax.set_xlabel("Year")
ax.set_ylabel("Life expectancy (years)")
ax.grid(axis="y", alpha=0.2)
plt.show()
"""),
            ("markdown", """### Fix B — selectively highlight countries

The highlighted chart retains all 142 country trajectories as context and directly labels three examples, without a legend. It lets a reader follow selected countries but does not summarize regional averages. Fix A is better for comparing broad groups; Fix B is better for illustrating a few individual paths.
"""),
            ("code", """
extremes = (
    df.loc[df.groupby("year")["gdpPercap"].idxmax(), ["year", "country", "gdpPercap"]]
    .rename(columns={"country": "richest_country", "gdpPercap": "richest_gdp_per_capita"})
    .merge(
        df.loc[df.groupby("year")["gdpPercap"].idxmin(), ["year", "country", "gdpPercap"]]
        .rename(columns={"country": "poorest_country", "gdpPercap": "poorest_gdp_per_capita"}),
        on="year",
    )
)
extremes["gap"] = extremes["richest_gdp_per_capita"] - extremes["poorest_gdp_per_capita"]
gap_change = (1 - extremes["gap"].iloc[-1] / extremes["gap"].iloc[0]) * 100

fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(extremes["year"], extremes["gap"], marker="o", color="#0F766E", linewidth=2.5)
ax.set_title(f"Richest–poorest GDP-per-capita gap narrowed {gap_change:.0f}% from 1952 to 2007")
ax.set_xlabel("Year")
ax.set_ylabel("GDP per capita difference (dataset units)")
ax.grid(axis="y", alpha=0.25)
plt.show()
extremes[["year", "richest_country", "poorest_country", "gap"]].round(1)
"""),
            ("markdown", """### Did the richest-poorest gap narrow?

For each year, this chart subtracts the lowest country's GDP per capita from the highest country's GDP per capita. In this dataset the absolute gap falls from about 108,084 in 1952 to about 49,080 in 2007. The countries at either extreme can change between years, so the line compares each year's range—not a fixed pair of countries. This is an absolute GDP-per-capita gap, not a ratio or a measure of within-country inequality.
"""),
            ("code", """
fig, axes = plt.subplots(1, 2, figsize=(13, 5), constrained_layout=True)
axes[0].hist(df["gdpPercap"], bins=35, color="#94A3B8", edgecolor="white")
axes[0].set_title("GDP per capita is strongly right-skewed")
axes[0].set_xlabel("GDP per capita (dataset units)")
axes[0].set_ylabel("Country-year rows")
axes[1].hist(df["gdpPercap"], bins=35, color="#0F766E", edgecolor="white")
axes[1].set_xscale("log")
axes[1].set_title("A logarithmic x-axis reveals lower-value detail")
axes[1].set_xlabel("GDP per capita (logarithmic scale)")
axes[1].set_ylabel("Country-year rows")
for ax in axes:
    ax.grid(axis="y", alpha=0.2)
fig.suptitle("The GDP-per-capita distribution has a long upper tail")
plt.show()
"""),
            ("markdown", """### Why use a logarithmic x-axis?

The raw histogram is compressed near the lower values by a small number of very high GDP-per-capita observations. A logarithmic x-axis spaces equal ratios evenly and makes the lower and middle distribution easier to inspect. It does not change the observations, but it changes visual distances: equal horizontal steps represent multiplicative rather than additive changes. Use and label it when comparing the shape; use the raw scale when absolute differences are the question.
"""),
        ],
    )


def task3() -> dict:
    return notebook(
        "Week 1 · Task 3 — Distributions and relationships",
        [
            ("code", DATA_SETUP + """
df = pd.read_csv(assignment_data("penguins.csv"))
measurement_columns = [
    "bill_length_mm",
    "bill_depth_mm",
    "flipper_length_mm",
    "body_mass_g",
]
missing_measurement_rows = int(df[measurement_columns].isna().any(axis=1).sum())
missing_sex_rows = int(df["sex"].isna().sum())
complete_measurements = df.dropna(subset=measurement_columns)
print(f"Rows in source: {len(df)}")
print(f"Rows with at least one missing measurement: {missing_measurement_rows}")
print(f"Rows with missing sex: {missing_sex_rows}")
print(f"Rows with complete measurements: {len(complete_measurements)}")
"""),
            ("markdown", """### Missing-data decision

Keep the original table unchanged. For each chart, remove only rows missing the fields that chart actually needs. This preserves usable penguins instead of dropping a row merely because an unrelated field is missing. The two rows with missing measurements and the eleven rows with missing sex are counted above; some rows may belong to both groups, so do not add those counts to infer a unique-row total.
"""),
            ("code", """
body_mass = df.dropna(subset=["body_mass_g"])
fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(body_mass["body_mass_g"], bins=25, color="#176B87", edgecolor="white")
ax.set_title("Penguin body mass has a broad, multi-peaked distribution")
ax.set_xlabel("Body mass (g)")
ax.set_ylabel("Penguins")
ax.text(
    0.99, 0.96,
    f"n = {len(body_mass)}; excluded {df['body_mass_g'].isna().sum()} rows missing body mass",
    transform=ax.transAxes, ha="right", va="top", fontsize=9,
)
ax.grid(axis="y", alpha=0.2)
plt.show()
"""),
            ("markdown", """### Reading the pooled body-mass distribution

The pooled histogram is broad and has multiple visible peaks rather than one compact mound. Each bar counts penguins in a body-mass interval. This plot excludes only the two rows without body mass; it retains penguins whose sex is unknown because sex is not needed for this question.
"""),
            ("code", """
species_order = ["Adelie", "Chinstrap", "Gentoo"]
fig, axes = plt.subplots(1, 3, figsize=(14, 4.5), sharex=True, sharey=True, constrained_layout=True)
for ax, species in zip(axes, species_order):
    group = body_mass.loc[body_mass["species"] == species]
    ax.hist(group["body_mass_g"], bins=18, color="#176B87", edgecolor="white")
    ax.set_title(f"{species} (n={len(group)})")
    ax.set_xlabel("Body mass (g)")
    ax.grid(axis="y", alpha=0.2)
axes[0].set_ylabel("Penguins")
fig.suptitle("Species occupy different body-mass ranges, creating pooled peaks")
plt.show()
"""),
            ("markdown", """### Does species explain the pooled shape?

Yes, to a substantial degree. The species-specific distributions occupy different mass ranges, especially the heavier Gentoo group, so combining them produces multiple peaks. The plotted samples include all rows with a measured body mass; unknown sex is not an exclusion for these histograms.
"""),
            ("code", """
bill_data = df.dropna(subset=["bill_length_mm", "bill_depth_mm", "species"])
overall_r = bill_data["bill_length_mm"].corr(bill_data["bill_depth_mm"])
species_r = pd.Series(
    {
        species: group["bill_length_mm"].corr(group["bill_depth_mm"])
        for species, group in bill_data.groupby("species", observed=True)
    }
)

fig, ax = plt.subplots(figsize=(9, 6))
colors = {"Adelie": "#2563EB", "Chinstrap": "#D97706", "Gentoo": "#0F766E"}
for species, group in bill_data.groupby("species", observed=True):
    color = colors[species]
    ax.scatter(
        group["bill_length_mm"], group["bill_depth_mm"],
        label=f"{species} (r={species_r[species]:.2f})",
        alpha=0.65, s=28, color=color,
    )
    slope, intercept = np.polyfit(group["bill_length_mm"], group["bill_depth_mm"], 1)
    x_line = np.linspace(group["bill_length_mm"].min(), group["bill_length_mm"].max(), 100)
    ax.plot(x_line, slope * x_line + intercept, color=color, linewidth=2)
slope, intercept = np.polyfit(bill_data["bill_length_mm"], bill_data["bill_depth_mm"], 1)
x_line = np.linspace(bill_data["bill_length_mm"].min(), bill_data["bill_length_mm"].max(), 100)
ax.plot(
    x_line, slope * x_line + intercept, color="#111827", linestyle="--", linewidth=2.5,
    label=f"All species (r={overall_r:.2f})",
)
ax.set_title("Pooled bill correlation is negative while every species trend is positive")
ax.set_xlabel("Bill length (mm)")
ax.set_ylabel("Bill depth (mm)")
ax.legend(frameon=False)
ax.grid(alpha=0.2)
ax.text(
    0.99, 0.02,
    f"n={len(bill_data)}; excludes {len(df) - len(bill_data)} rows missing bill measurements",
    transform=ax.transAxes, ha="right", va="bottom", fontsize=9,
)
plt.show()
print(f"Overall Pearson correlation: {overall_r:.3f}")
print("Within-species Pearson correlations:")
display(species_r.rename("correlation").to_frame().round(3))
"""),
            ("markdown", """### Simpson's paradox: why the pooled slope changes

Across all measured penguins, bill length and bill depth have a modest negative correlation (about −0.24). Within each species, the correlations are positive (roughly 0.39 for Adelie, 0.65 for Chinstrap, and 0.64 for Gentoo). The dashed black line is the pooled fit; colored lines are within-species fits.

Species differ in their typical bill sizes and group locations. Pooling those groups combines within-species relationships with between-species differences, producing a direction that differs from every within-group relationship. This is Simpson's paradox. The plot excludes the two rows missing bill measurements; missing sex is irrelevant here and those rows are retained if their bill measurements exist.
"""),
            ("code", """
mass_sex = df.dropna(subset=["species", "sex", "body_mass_g"])
mass_summary = (
    mass_sex.groupby(["species", "sex"], observed=True)["body_mass_g"]
    .agg(mean_mass="mean", sd_mass="std", count="count")
    .reset_index()
)

fig, ax = plt.subplots(figsize=(10, 5.5))
x = np.arange(len(species_order))
width = 0.36
for offset, sex, color in [(-width / 2, "Female", "#D1495B"), (width / 2, "Male", "#176B87")]:
    group = mass_summary.loc[mass_summary["sex"].str.title() == sex].set_index("species").reindex(species_order)
    ax.bar(
        x + offset, group["mean_mass"], width,
        yerr=group["sd_mass"], capsize=4, color=color, label=sex,
    )
    for xpos, (_, row) in zip(x + offset, group.iterrows()):
        ax.text(xpos, row["mean_mass"] + row["sd_mass"] + 25, f"n={int(row['count'])}", ha="center", fontsize=8)
ax.set_xticks(x, species_order)
ax.set_title("Mean body mass differs by both species and sex")
ax.set_xlabel("Species")
ax.set_ylabel("Mean body mass (g)")
ax.legend(title="Sex", frameon=False)
ax.text(
    0.99, 0.02,
    f"n={len(mass_sex)}; excludes {len(df) - len(mass_sex)} rows with missing sex or body mass",
    transform=ax.transAxes, ha="right", va="bottom", fontsize=9,
)
ax.grid(axis="y", alpha=0.2)
plt.show()
mass_summary.round(1)
"""),
            ("markdown", """### Average body mass across species and sex

The grouped bars compare mean body mass for each species-sex combination; error bars show one standard deviation and labels show group sample sizes. The chart uses rows with known species, sex, and body mass. It explicitly reports the rows excluded because sex or body mass is missing, rather than silently dropping them.
"""),
        ],
    )


def task4() -> dict:
    return notebook(
        "Week 1 · Task 4 — Pick the right chart, five times",
        [
            ("code", DATA_SETUP + """
df = pd.read_csv(assignment_data("mpg.csv"))
missing_horsepower = int(df["horsepower"].isna().sum())
print(f"Source rows: {len(df)}")
print(f"Missing horsepower values: {missing_horsepower}")
print("Horsepower is not used in the five questions below, so those rows are retained.")
"""),
            ("code", """
mpg_by_year = df.groupby("model_year", as_index=False)["mpg"].mean()
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(mpg_by_year["model_year"] + 1900, mpg_by_year["mpg"], marker="o", color="#176B87", linewidth=2.5)
ax.set_title("Average fuel efficiency rose from 17.7 to 31.7 MPG")
ax.set_xlabel("Model year")
ax.set_ylabel("Mean fuel efficiency (MPG)")
ax.grid(axis="y", alpha=0.2)
plt.show()
"""),
            ("markdown", """### 1 · Did cars get more fuel-efficient?

A line chart fits an ordered year trend. Mean MPG rises from about 17.7 in model year 1970 to about 31.7 in 1982. The calculation uses every row with MPG and model year; missing horsepower does not affect it.
"""),
            ("code", """
origin_order = ["usa", "europe", "japan"]
origin_names = {"usa": "USA", "europe": "Europe", "japan": "Japan"}
fig, ax = plt.subplots(figsize=(9, 5))
groups = [
    df.loc[df["origin"] == origin, "mpg"].dropna().to_numpy()
    for origin in origin_order
]
labels = [origin_names[origin] for origin in origin_order]
ax.boxplot(groups, tick_labels=labels, patch_artist=True, medianprops={"color": "#111827", "linewidth": 2})
for patch, color in zip(ax.patches, ["#94A3B8", "#D97706", "#0F766E"]):
    patch.set_facecolor(color)
    patch.set_alpha(0.75)
ax.set_title("Japanese and European cars typically achieve higher MPG than US cars")
ax.set_xlabel("Origin")
ax.set_ylabel("Fuel efficiency (MPG)")
ax.grid(axis="y", alpha=0.2)
plt.show()
"""),
            ("markdown", """### 2 · Do origins differ in fuel efficiency?

A box plot compares the distributions, medians, and spread of MPG across the three origin groups. Japanese and European cars generally have higher MPG distributions than US cars, though distributions overlap. A distribution chart is more informative than comparing means alone.
"""),
            ("code", """
fig, ax = plt.subplots(figsize=(9, 5.5))
ax.scatter(df["weight"], df["mpg"], alpha=0.55, s=28, color="#0F766E", edgecolors="none")
ax.set_title("Heavier cars tend to have lower fuel efficiency")
ax.set_xlabel("Weight (lb)")
ax.set_ylabel("Fuel efficiency (MPG)")
ax.grid(alpha=0.2)
plt.show()
"""),
            ("markdown", """### 3 · How are weight and fuel efficiency related?

A scatter plot is appropriate for two quantitative variables. The clear downward association indicates that heavier cars tend to have lower MPG. The plot shows association, not proof that weight alone causes the difference.
"""),
            ("code", """
cylinder_counts = df["cylinders"].value_counts().sort_index()
most_common_cylinders = int(cylinder_counts.idxmax())
most_common_count = int(cylinder_counts.max())
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(cylinder_counts.index.astype(str), cylinder_counts.values, color="#176B87")
ax.bar_label(bars, padding=3)
ax.set_title(
    f"{most_common_cylinders}-cylinder cars are most common "
    f"({most_common_count} of {len(df)} cars)"
)
ax.set_xlabel("Number of cylinders")
ax.set_ylabel("Number of cars")
ax.set_ylim(0, cylinder_counts.max() * 1.15)
ax.grid(axis="y", alpha=0.2)
plt.show()
"""),
            ("markdown", """### 4 · How are cylinder counts distributed?

A bar chart compares counts for the discrete cylinder categories. Eight-cylinder cars are the largest group in this dataset; the bar labels make the sample counts explicit.
"""),
            ("code", """
weight_by_year = df.groupby("model_year", as_index=False)["weight"].mean()
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(weight_by_year["model_year"] + 1900, weight_by_year["weight"], marker="o", color="#D1495B", linewidth=2.5)
ax.set_title("Average car weight fell from about 3,373 lb to 2,454 lb")
ax.set_xlabel("Model year")
ax.set_ylabel("Mean weight (lb)")
ax.grid(axis="y", alpha=0.2)
plt.show()
"""),
            ("markdown", """### 5 · Did cars get lighter?

Yes, the yearly mean weight drops from approximately 3,373 lb in 1970 to 2,454 lb in 1982. Together with the MPG trend and weight-MPG scatter, this is consistent with lighter cars contributing to better fuel efficiency. The charts alone do not establish how much of the MPG improvement is caused by weight rather than engine, technology, or fleet composition.
"""),
            ("code", """
fig, ax = plt.subplots(figsize=(9, 5.5))
ax.scatter(df["weight"], df["mpg"], alpha=0.3, s=24, color="#94A3B8", label="Cars")
slope, intercept = np.polyfit(df["weight"], df["mpg"], 1)
x_line = np.linspace(df["weight"].min(), df["weight"].max(), 100)
ax.plot(x_line, slope * x_line + intercept, color="#D1495B", linewidth=3, label="Linear trend")
ax.set_title("A fitted line clarifies the negative weight–MPG association")
ax.set_xlabel("Weight (lb)")
ax.set_ylabel("Fuel efficiency (MPG)")
ax.legend(frameon=False)
ax.grid(alpha=0.2)
plt.show()
"""),
            ("markdown", """### Redrawing the weakest chart

The original weight-versus-MPG scatter can look busy because many points overlap. This redraw uses lighter points and a clearly labeled linear trend line. It improves the visibility of the overall direction but does not imply a causal model or capture every nonlinear pattern.

All five questions use the available rows for their own fields. Six rows have missing horsepower, but horsepower is not part of these five calculations, so those rows are retained rather than dropped. The dashboard titles state the findings instead of repeating axis names.
"""),
        ],
    )


def task5() -> dict:
    return notebook(
        "Week 1 · Task 5 — A real time series",
        [
            ("code", DATA_SETUP + """
df = pd.read_csv(assignment_data("flights.csv"))
df["date"] = pd.to_datetime(
    df["year"].astype(str) + "-" + df["month"],
    format="%Y-%B",
    errors="coerce",
)
assert df["date"].notna().all()
df = df.sort_values("date").reset_index(drop=True)
df["month_num"] = df["date"].dt.month
df["month_name"] = df["date"].dt.month_name()
"""),
            ("code", """
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(df["date"], df["passengers"], color="#176B87", linewidth=2.2)
ax.set_title("Monthly airline passengers increased steadily from 1949 to 1960")
ax.set_xlabel("Month")
ax.set_ylabel("Passengers (thousands)")
ax.grid(axis="y", alpha=0.2)
plt.show()
"""),
            ("markdown", """### 1 · Trend over time

Combining year and month into a real datetime creates one correctly ordered monthly axis. The series shows sustained growth, with a repeating seasonal cycle layered on top.
"""),
            ("code", """
month_order = list(range(1, 13))
month_labels = [pd.Timestamp(2000, month, 1).strftime("%b") for month in month_order]
seasonal = df.pivot(index="month_num", columns="year", values="passengers").reindex(month_order)

fig, ax = plt.subplots(figsize=(12, 6))
for year in seasonal.columns:
    ax.plot(month_labels, seasonal[year], linewidth=1.2, alpha=0.65, label=str(year))
ax.set_title("Passenger totals rise through the year, with a strong summer peak")
ax.set_xlabel("Month")
ax.set_ylabel("Passengers (thousands)")
ax.legend(title="Year", bbox_to_anchor=(1.02, 1), loc="upper left", ncol=2, fontsize=8, frameon=False)
ax.grid(axis="y", alpha=0.2)
plt.show()
"""),
            ("markdown", """### 2 · Seasonal cycle by year

Each line is one calendar year and the horizontal axis is month. This chart aligns the years to expose the recurring seasonal shape; it is not intended to show the chronological order across all 144 months.
"""),
            ("code", """
mean_by_month = df.groupby("month_num")["passengers"].mean().reindex(month_order)
busiest_month = int(mean_by_month.idxmax())
colors = ["#0F766E" if month == busiest_month else "#CBD5E1" for month in month_order]

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(month_labels, mean_by_month.values, color=colors)
ax.bar_label(bars, fmt="%.0f", padding=3, fontsize=8)
ax.set_title(f"{month_labels[busiest_month - 1]} is the busiest month on average")
ax.set_xlabel("Month")
ax.set_ylabel("Mean passengers (thousands)")
ax.tick_params(axis="x", rotation=35)
ax.set_ylim(0, mean_by_month.max() * 1.15)
ax.grid(axis="y", alpha=0.2)
plt.show()
"""),
            ("markdown", """### 3 · Which month is busiest?

July has the highest average passenger total across the 12 years. This bar chart answers a focused month-of-year comparison; it intentionally averages away the year-by-year growth.
"""),
            ("markdown", """### 4 · Which chart belongs in a report?

For a report whose main message is that passenger totals grew over time, I would lead with the chronological time-series chart. It keeps the actual sequence and makes the long-term rise clear. The seasonal-by-year chart is useful as a supporting figure when the seasonal pattern matters, but it is more crowded. The monthly-average bars are best for the narrower question of which month is busiest; they hide the individual years and long-term growth. These charts answer different questions, so they should not all be placed together without a specific reason.
"""),
            ("code", """
annual_mean = df.groupby("year")["passengers"].transform("mean")
df["seasonal_index"] = 100 * df["passengers"] / annual_mean
relative = df.pivot(index="month_num", columns="year", values="seasonal_index").reindex(month_order)

fig, ax = plt.subplots(figsize=(12, 5.5))
for year in relative.columns:
    ax.plot(month_labels, relative[year], color="#176B87", alpha=0.35, linewidth=1)
monthly_index = relative.mean(axis=1)
ax.plot(month_labels, monthly_index, color="#D1495B", linewidth=3, marker="o", label="Average seasonal index")
ax.axhline(100, color="#334155", linestyle="--", linewidth=1.3, label="Annual mean = 100")
ax.set_title("Seasonal shape after removing each year's overall passenger level")
ax.set_xlabel("Month")
ax.set_ylabel("Passengers as % of that year's mean")
ax.legend(frameon=False)
ax.grid(axis="y", alpha=0.2)
plt.show()

relative_amplitude = (relative.max(axis=0) - relative.min(axis=0))
print(
    "Relative seasonal amplitude (max monthly index - min monthly index): "
    f"{relative_amplitude.iloc[0]:.1f} points in {relative_amplitude.index[0]} vs "
    f"{relative_amplitude.iloc[-1]:.1f} points in {relative_amplitude.index[-1]}."
)
"""),
            ("markdown", """### Is the seasonal swing growing, or is the airline growing?

The raw passenger swing can increase simply because the whole airline is larger. The final chart divides each month's passengers by that year's average and scales the result to 100. If the normalized seasonal curves have similar ranges over time, the larger raw swing is mainly consistent with overall growth; a widening normalized range would suggest seasonality is also strengthening. This index chart is the appropriate comparison because it removes the annual level before comparing seasonal amplitude.
"""),
        ],
    )


def main() -> None:
    notebooks = [task1(), task2(), task3(), task4(), task5()]
    for number, content in enumerate(notebooks, start=1):
        destination = ROOT / f"task{number}.ipynb"
        destination.write_text(json.dumps(content, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"Created {destination}")


if __name__ == "__main__":
    main()
