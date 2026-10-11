from pathlib import Path
import json

root = Path("d:/7_Semester/data-visualization/week1")


def new_markdown(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(True)}


def new_code(code):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": code.splitlines(True)}


def notebook(*cells):
    return {
        "cells": [
            new_markdown("# Week 1 Task " + cells[0][0] if False else "# Week 1 Task")
        ],
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.11"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def build_task(task_num, title, cells):
    nb = {
        "cells": [new_markdown(f"# Week 1 Task {task_num} — {title}\n\nThis notebook follows the Week 1 assignment brief and keeps each task in a separate file."), *[new_code(c) for c in cells]],
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.11"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    return nb


def main():
    task1 = build_task(
        1,
        "Prove why we visualize",
        [
            "from pathlib import Path\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\npath = Path('week1/assignments/data/datasaurus.csv')\nif not path.exists():\n    path = Path('assignments/data/datasaurus.csv')\nif not path.exists():\n    path = Path('d:/7_Semester/data-visualization/week1/assignments/data/datasaurus.csv')\n\ndf = pd.read_csv(path)\nsummary = df.groupby('dataset').apply(lambda g: pd.Series({\n    'x_mean': g['x'].mean(),\n    'y_mean': g['y'].mean(),\n    'x_sd': g['x'].std(ddof=1),\n    'y_sd': g['y'].std(ddof=1),\n    'corr': g['x'].corr(g['y'])\n})).reset_index()\nsummary.round(3)",
            "fig, axes = plt.subplots(4, 4, figsize=(16, 12), constrained_layout=True)\nfor ax, (name, group) in zip(axes.flat, df.groupby('dataset')):\n    ax.scatter(group['x'], group['y'], s=8, color='#4c72b0', alpha=0.8)\n    ax.set_title(name)\n    ax.set_xticks([])\n    ax.set_yticks([])\n    ax.set_aspect('equal', adjustable='box')\nfor ax in axes.flat[len(df['dataset'].unique()):]:\n    ax.set_visible(False)\nfig.suptitle('All 13 datasets in the Datasaurus collection', fontsize=16, y=1.02)\nplt.show()",
            "# The summary statistics are nearly identical across datasets, but the scatter plots show different shapes. This proves that summary statistics alone can hide important structure and that visualizing the data is essential.",
        ],
    )

    task2 = build_task(
        2,
        "Trends and the spaghetti problem",
        [
            "from pathlib import Path\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\npath = Path('week1/assignments/data/gapminder.csv')\nif not path.exists():\n    path = Path('assignments/data/gapminder.csv')\nif not path.exists():\n    path = Path('d:/7_Semester/data-visualization/week1/assignments/data/gapminder.csv')\n\ndf = pd.read_csv(path)\nfig, ax = plt.subplots(figsize=(14, 7))\nfor country, group in df.groupby('country'):\n    ax.plot(group['year'], group['lifeExp'], alpha=0.25, color='tab:blue')\nax.set_title('Life expectancy over time: every country plotted')\nax.set_xlabel('Year')\nax.set_ylabel('Life expectancy (years)')\nplt.show()",
            "continent = df.groupby(['continent', 'year'], as_index=False)['lifeExp'].mean()\nfig, ax = plt.subplots(figsize=(12, 6))\nfor name, g in continent.groupby('continent'):\n    ax.plot(g['year'], g['lifeExp'], marker='o', linewidth=2, label=name)\nax.set_title('Average life expectancy by continent')\nax.set_xlabel('Year')\nax.set_ylabel('Life expectancy (years)')\nax.legend()\nplt.show()",
            "interesting = ['Afghanistan', 'Japan', 'United States']\nfig, ax = plt.subplots(figsize=(12, 6))\nfor country, group in df.groupby('country'):\n    if country in interesting:\n        color = {'Afghanistan': '#d62728', 'Japan': '#2ca02c', 'United States': '#1f77b4'}[country]\n        ax.plot(group['year'], group['lifeExp'], color=color, linewidth=2.5, label=country)\n        ax.text(group['year'].iloc[-1], group['lifeExp'].iloc[-1], country, va='bottom', ha='left')\n    else:\n        ax.plot(group['year'], group['lifeExp'], color='lightgray', linewidth=1)\nax.set_title('Life expectancy over time with selective highlighting')\nax.set_xlabel('Year')\nax.set_ylabel('Life expectancy (years)')\nax.legend().remove()\nplt.show()",
            "# The spaghetti plot is too crowded to read, while the grouped chart makes the broad trend clear. Highlighting a few countries keeps the country-level story while removing the visual noise.",
        ],
    )

    task3 = build_task(
        3,
        "Distributions and relationships",
        [
            "from pathlib import Path\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\npath = Path('week1/assignments/data/penguins.csv')\nif not path.exists():\n    path = Path('assignments/data/penguins.csv')\nif not path.exists():\n    path = Path('d:/7_Semester/data-visualization/week1/assignments/data/penguins.csv')\n\ndf = pd.read_csv(path)\nprint(df.isnull().sum())\nclean = df.dropna(subset=['body_mass_g', 'bill_length_mm', 'bill_depth_mm', 'sex']).copy()\nprint(f'Rows kept: {len(clean)} / {len(df)}')",
            "fig, ax = plt.subplots(figsize=(10, 5))\nax.hist(clean['body_mass_g'], bins=25, color='steelblue', edgecolor='black')\nax.set_title('Distribution of penguin body mass')\nax.set_xlabel('Body mass (g)')\nax.set_ylabel('Count')\nplt.show()",
            "fig, ax = plt.subplots(figsize=(10, 5))\nfor species, group in clean.groupby('species'):\n    ax.hist(group['body_mass_g'], bins=20, alpha=0.5, label=species)\nax.set_title('Body mass distribution by species')\nax.set_xlabel('Body mass (g)')\nax.set_ylabel('Count')\nax.legend()\nplt.show()",
            "fig, ax = plt.subplots(figsize=(8, 6))\nfor species, group in clean.groupby('species'):\n    ax.scatter(group['bill_length_mm'], group['bill_depth_mm'], label=species, alpha=0.7)\nax.set_title('Bill length vs bill depth by species')\nax.set_xlabel('Bill length (mm)')\nax.set_ylabel('Bill depth (mm)')\nax.legend()\nplt.show()",
            "# This shows Simpson's paradox: the overall relationship is negative, but within each species it is positive. Grouping by species separates the confounding effect and makes the real pattern visible.",
        ],
    )

    task4 = build_task(
        4,
        "Pick the right chart, five times",
        [
            "from pathlib import Path\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\npath = Path('week1/assignments/data/mpg.csv')\nif not path.exists():\n    path = Path('assignments/data/mpg.csv')\nif not path.exists():\n    path = Path('d:/7_Semester/data-visualization/week1/assignments/data/mpg.csv')\n\ndf = pd.read_csv(path).dropna(subset=['horsepower'])\nmean_mpg_by_year = df.groupby('model_year')['mpg'].mean()\nfig, ax = plt.subplots(figsize=(10, 5))\nax.plot(mean_mpg_by_year.index, mean_mpg_by_year.values, marker='o', linewidth=2, color='tab:blue')\nax.set_title('Fuel efficiency improved over the period')\nax.set_xlabel('Model year')\nax.set_ylabel('Mean MPG')\nplt.show()",
            "fig, ax = plt.subplots(figsize=(8, 5))\ndf.boxplot(column='mpg', by='origin', ax=ax)\nax.set_title('Fuel efficiency by region of origin')\nax.set_xlabel('Origin')\nax.set_ylabel('MPG')\nplt.show()",
            "fig, ax = plt.subplots(figsize=(8, 5))\nax.scatter(df['weight'], df['mpg'], alpha=0.7, color='darkgreen')\nax.set_title('Heavier cars are less fuel-efficient')\nax.set_xlabel('Weight')\nax.set_ylabel('MPG')\nplt.show()",
            "fig, ax = plt.subplots(figsize=(8, 5))\ndf['cylinders'].value_counts().sort_index().plot(kind='bar', ax=ax, color='salmon')\nax.set_title('Distribution of cylinder counts')\nax.set_xlabel('Cylinders')\nax.set_ylabel('Number of cars')\nplt.show()",
            "# Different chart types are appropriate for different questions. The key is the data relationship: trend over time uses a line, distribution uses a bar or boxplot, and relationship uses a scatter.",
        ],
    )

    task5 = build_task(
        5,
        "A real time series",
        [
            "from pathlib import Path\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\npath = Path('week1/assignments/data/flights.csv')\nif not path.exists():\n    path = Path('assignments/data/flights.csv')\nif not path.exists():\n    path = Path('d:/7_Semester/data-visualization/week1/assignments/data/flights.csv')\n\nmonth_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']\nmonth_map = {m: i for i, m in enumerate(month_order)}\ndf = pd.read_csv(path)\ndf['month_num'] = df['month'].map(month_map)\ndf['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month_num'].astype(str).str.zfill(2) + '-01')\ndf = df.sort_values('date').reset_index(drop=True)\nfig, ax = plt.subplots(figsize=(12, 5))\nax.plot(df['date'], df['passengers'], color='tab:blue', marker='o')\nax.set_title('Monthly airline passengers over time')\nax.set_xlabel('Date')\nax.set_ylabel('Passengers')\nplt.show()",
            "seasonal = df.pivot_table(index='month', columns='year', values='passengers', aggfunc='first').reindex(month_order)\nfig, ax = plt.subplots(figsize=(12, 6))\nfor year in seasonal.columns:\n    ax.plot(seasonal.index, seasonal[year], marker='o', linewidth=1.5, alpha=0.8, label=str(year))\nax.set_title('Seasonal pattern by year')\nax.set_xlabel('Month')\nax.set_ylabel('Passengers')\nax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)\nplt.show()",
            "mean_by_month = df.groupby('month', observed=False)['passengers'].mean().reindex(month_order)\nfig, ax = plt.subplots(figsize=(10, 5))\nax.bar(mean_by_month.index, mean_by_month.values, color='tomato')\nax.set_title('Average monthly passengers')\nax.set_xlabel('Month')\nax.set_ylabel('Average passengers')\nplt.xticks(rotation=45)\nplt.show()",
            "# The first chart captures long-term growth, the second isolates the seasonal pattern, and the third makes the busiest month obvious. The seasonal swing can be larger simply because the level of traffic is larger, so a chart of monthly index values or a decomposition would help separate the two effects.",
        ],
    )

    for task_num, nb in enumerate([task1, task2, task3, task4, task5], start=1):
        out_path = root / f'task{task_num}.ipynb'
        with out_path.open('w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1)
        print(f'Created {out_path}')


if __name__ == '__main__':
    main()
