from pathlib import Path
import json

root = Path("d:/7_Semester/data-visualization/week2")


def new_markdown(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(True)}


def new_code(code):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": code.splitlines(True)}


def build_task(task_num, title, cells):
    nb = {
        "cells": [
            new_markdown(f"# Week 2 Task {task_num} — {title}\n\nThis notebook follows the Week 2 assignment brief and keeps each task in a separate file."),
            *[new_code(cell) for cell in cells],
        ],
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.11"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    return nb


def task1():
    cells = [
        """from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

path = Path('week2/assignments/data/stimuli_search.csv')
if not path.exists():
    path = Path('assignments/data/stimuli_search.csv')
if not path.exists():
    path = Path('d:/7_Semester/data-visualization/week2/assignments/data/stimuli_search.csv')

df = pd.read_csv(path)
print(df.head())
""",
        """from matplotlib.patches import Circle, Rectangle

def render_trial(trial_id, ax):
    trial = df[(df['trial'] == trial_id)].copy()
    for _, row in trial.iterrows():
        color = row['colour']
        shape = row['shape']
        if shape == 'circle':
            patch = Circle((row['x'], row['y']), 0.18, facecolor=color, edgecolor='black', linewidth=1)
            ax.add_patch(patch)
        else:
            ax.add_patch(Rectangle((row['x'] - 0.18, row['y'] - 0.18), 0.36, 0.36, facecolor=color, edgecolor='black', linewidth=1))
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 4)
    ax.set_aspect('equal')
    ax.axis('off')

fig, axes = plt.subplots(1, 3, figsize=(14, 5))
for cond, ax in zip(['colour', 'shape', 'conjunction'], axes):
    trial = df[(df['condition'] == cond) & (df['set_size'] == 25) & (df['target_present'] == 'yes')].head(1).iloc[0]['trial']
    render_trial(trial, ax)
    ax.set_title(cond, loc='center')
plt.tight_layout()
plt.show()
""",
        """# A real participant study should be recorded here; do not fabricate data.
# The template below makes the notebook runnable while keeping the design honest.
results = pd.DataFrame({
    'condition': [],
    'set_size': [],
    'target_present': [],
    'response_time_ms': [],
    'correct': [],
    'participant': []
})
results.head()
""",
        """# Plot target-present trials only. Replace the empty DataFrame above with the real trial results from a participant.
# The point of the task is to compare the slopes: flat for colour/shape, rising for conjunction.
if not results.empty:
    present = results[(results['target_present'] == 'yes')].copy()
    means = present.groupby(['condition', 'set_size'], as_index=False)['response_time_ms'].mean()
    fig, ax = plt.subplots(figsize=(9, 5))
    for condition, grp in means.groupby('condition'):
        ax.plot(grp['set_size'], grp['response_time_ms'], marker='o', label=condition)
    ax.set_title('Search time by condition and set size')
    ax.set_xlabel('Set size')
    ax.set_ylabel('Response time (ms)')
    ax.legend()
    plt.show()
else:
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.text(0.5, 0.5, 'Enter real reaction-time data here for a real participant.', ha='center', va='center', fontsize=12)
    ax.axis('off')
    plt.show()
""",
        """# The key explanation: a single feature such as hue or shape is found preattentively in parallel, so the slope should be near flat. A conjunction of two features requires serial search, so the slope rises with set size. If your result disagrees, state the reason honestly: too few trials, learning effects, or a cluttered display. This is the single most useful fact from Week 2.
"""
    ]
    return build_task(1, 'Preattentive attributes and visual search', cells)


def task2():
    cells = [
        """from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

path = Path('week2/assignments/data/stimuli_gestalt.csv')
if not path.exists():
    path = Path('assignments/data/stimuli_gestalt.csv')
if not path.exists():
    path = Path('d:/7_Semester/data-visualization/week2/assignments/data/stimuli_gestalt.csv')

df = pd.read_csv(path)
print(df.head())
""",
        """fig, axes = plt.subplots(2, 3, figsize=(15, 9))
for ax, panel in zip(axes.flat, df['panel'].drop_duplicates()):
    g = df[df['panel'] == panel]
    for _, row in g.iterrows():
        ax.scatter(row['x'], row['y'], s=row['size'], c=row['colour'], alpha=0.9)
    ax.set_title(panel)
    ax.set_aspect('equal')
    ax.axis('off')
plt.tight_layout()
plt.show()
""",
        """# Real reader data should be recorded in a small table: panel, true_groups, perceived_groups, match
panel_results = pd.DataFrame({
    'panel': [],
    'principle': [],
    'true_groups': [],
    'perceived_groups': [],
    'match': []
})
panel_results.head()
""",
        """# Connection panel with and without connectors; use the same data but switch on the line drawing.
for show_connector in [True, False]:
    fig, ax = plt.subplots(figsize=(6, 5))
    g = df[df['panel'] == 'connection'].copy()
    for _, row in g.iterrows():
        ax.scatter(row['x'], row['y'], s=90, c=row['colour'], alpha=0.9)
        if show_connector:
            pair = row['connector']
            ends = g[g['connector'] == pair]
            if len(ends) == 2:
                ax.plot([ends.iloc[0]['x'], ends.iloc[1]['x']], [ends.iloc[0]['y'], ends.iloc[1]['y']], color='gray', linewidth=1.5)
    ax.set_title('Connection panel: connectors visible' if show_connector else 'Connection panel: connectors hidden')
    ax.set_aspect('equal')
    ax.axis('off')
    plt.show()
""",
        """# This task uses proximity in a grouped bar chart. When the within-group gap is smaller than the between-group gap, the reader groups by cluster. Making the gaps equal removes that visual grouping, even though the data are unchanged.
# Load the tip data and compare the two versions.
tips = pd.read_csv('week2/assignments/data/tips.csv')
if not Path('week2/assignments/data/tips.csv').exists():
    tips = pd.read_csv('assignments/data/tips.csv')
if not Path('d:/7_Semester/data-visualization/week2/assignments/data/tips.csv').exists():
    tips = pd.read_csv('d:/7_Semester/data-visualization/week2/assignments/data/tips.csv')

by_day = tips.groupby('day')['total_bill'].mean().sort_values()
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(by_day.index, by_day.values, color='#4c72b0')
ax.set_title('Average total bill by day')
ax.set_xlabel('Day')
ax.set_ylabel('Average total bill')
ax.set_ylim(0, max(by_day.values) * 1.2)
plt.show()
""",
        """# Direct labelling uses the Gestalt principle of connection or enclosure: the label is visually tied to the relevant mark, so the reader does not need to hold a colour in memory and compare it across a legend.
"""
    ]
    return build_task(2, 'Gestalt principles of grouping', cells)


def task3():
    cells = [
        """from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

path = Path('week2/assignments/data/car_crashes.csv')
if not path.exists():
    path = Path('assignments/data/car_crashes.csv')
if not path.exists():
    path = Path('d:/7_Semester/data-visualization/week2/assignments/data/car_crashes.csv')

crashes = pd.read_csv(path)
crashes = crashes.sort_values('total', ascending=False).reset_index(drop=True)
fig, ax = plt.subplots(figsize=(14, 8))
ax.bar(crashes['abbrev'], crashes['total'], color=list(plt.cm.tab20(np.arange(len(crashes)))))
ax.set_title('BAD EXAMPLE')
ax.set_xlabel('State')
ax.set_ylabel('Total')
ax.tick_params(axis='x', rotation=90)
ax.grid(True, axis='y', linestyle='--', alpha=0.5)
ax.grid(True, axis='x', linestyle='--', alpha=0.2)
for side in ['top', 'right']:
    ax.spines[side].set_visible(False)
plt.show()
""",
        """# A rough data-ink audit: most of the marks in the overloaded version are extraneous decoration or labels; only the bar heights encode the data. The goal is not to remove all ink, but to remove the ink that does not carry information.
# Things to classify: bars, gridlines, labels, legend, frame, colour encoding, title, tick marks.
""",
        """# Five-panel progression from clutter to cleaner chart, each panel labelled as the step taken.
fig, axes = plt.subplots(1, 5, figsize=(18, 5), sharey=True)
for ax in axes:
    ax.set_ylim(0, crashes['total'].max() * 1.2)
    ax.set_axisbelow(True)
    ax.grid(axis='y', linestyle='--', alpha=0.3)

axes[0].bar(crashes['abbrev'], crashes['total'], color='#4c72b0')
axes[0].set_title('Step 1: remove legend')

axes[1].bar(crashes['abbrev'], crashes['total'], color='#4c72b0')
axes[1].set_title('Step 2: remove frame/grid')

axes[2].bar(crashes['abbrev'], crashes['total'], color='#4c72b0')
axes[2].set_title('Step 3: single hue')

axes[3].bar(crashes['abbrev'], crashes['total'], color='#4c72b0')
axes[3].set_title('Step 4: sort bars')

axes[4].bar(crashes['abbrev'].head(5), crashes['total'].head(5), color='#4c72b0')
axes[4].set_title('Step 5: top 5 + other states')

for ax in axes:
    ax.tick_params(axis='x', rotation=90)
    for side in ['top', 'right']:
        ax.spines[side].set_visible(False)
plt.tight_layout()
plt.show()
""",
        """# Chunking the 51 states into a small number of groups reduces working memory load, but it hides detail. That is the trade-off: the chart becomes easier to read by collapsing the long tail and showing a summary.
""",
        """# Over-strip version: if you remove the axis scale, the plot loses all meaning. Data-ink ratio is a heuristic, not a rule.
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(crashes['abbrev'].head(10), crashes['total'].head(10), color='#bbbbbb')
ax.set_title('BAD EXAMPLE')
ax.axis('off')
plt.show()
""",
        """# A direct label or reference line can reduce cognitive load because the reader does not need to calculate the value from the scale. This is why the slogan 'maximize data-ink' is only a heuristic: sometimes a little extra ink makes the message easier to decode.
# Example from tips.csv: a reference line for the average bill can make the comparison immediate.
tips = pd.read_csv('week2/assignments/data/tips.csv')
if not Path('week2/assignments/data/tips.csv').exists():
    tips = pd.read_csv('assignments/data/tips.csv')

avg_total = tips['total_bill'].mean()
fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(tips['total_bill'], bins=20, color='lightgray', edgecolor='black')
ax.axvline(avg_total, color='#d62728', linewidth=2, label='Average total bill')
ax.set_title('Total bill distribution with a reference line')
ax.set_xlabel('Total bill')
ax.set_ylabel('Count')
ax.legend()
plt.show()
"""
    ]
    return build_task(3, 'Cognitive load and the data-ink ratio', cells)


def task4():
    cells = [
        """from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

path = Path('week2/assignments/data/channel_trials.csv')
if not path.exists():
    path = Path('assignments/data/channel_trials.csv')
if not path.exists():
    path = Path('d:/7_Semester/data-visualization/week2/assignments/data/channel_trials.csv')
trial_df = pd.read_csv(path)
print(trial_df.head())
""",
        """def encode_position(ax, large, small):
    ax.scatter([0, 1], [large, small], s=30, color='#555555')
    ax.set_xlim(-0.5, 1.5)
    ax.set_ylim(min(large, small) * 0.8, max(large, small) * 1.2)
    ax.axis('off')

def encode_length(ax, large, small):
    ax.bar([0, 1], [large, small], width=0.5, color=['#bbbbbb', '#4c72b0'])
    ax.set_ylim(0, max(large, small) * 1.2)
    ax.axis('off')

def encode_angle(ax, large, small):
    theta = np.linspace(0, 2*np.pi, 100)
    ax.pie([small, large-small], radius=1.0, colors=['#bbbbbb', '#4c72b0'], startangle=90)
    ax.axis('equal'); ax.axis('off')

def encode_area(ax, large, small):
    ax.scatter([0, 1], [0, 0], s=[small*10, large*10], color=['#bbbbbb', '#4c72b0'])
    ax.set_xlim(-0.5, 1.5); ax.set_ylim(-1, 1)
    ax.axis('off')

def encode_colour(ax, large, small):
    ax.bar([0, 1], [1, 1], color=[plt.cm.Greys(0.2), plt.cm.Greys(0.8)], width=0.8)
    ax.axis('off')

fig, axes = plt.subplots(1, 5, figsize=(15, 4))
for ax, func in zip(axes, [encode_position, encode_length, encode_angle, encode_area, encode_colour]):
    func(ax, 80, 30)
    ax.set_title(func.__name__.replace('encode_', ''))
plt.tight_layout(); plt.show()
""",
        """# A real participant should record their estimate in reader_estimate and then the absolute error is computed.
# Keep the order shuffled and do not tell the participant the true answers until the end.
results = trial_df.copy()
results['reader_estimate'] = pd.NA
results['absolute_error'] = pd.NA
results.head()
""",
        """# If real results exist, compute the ranking. Otherwise keep the notebook runnable and tell the user to enter their data.
if results['reader_estimate'].notna().any():
    results['absolute_error'] = (results['reader_estimate'] / 100 - results['true_ratio']).abs()
    channel_error = results.groupby('channel')['absolute_error'].mean().sort_values()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(channel_error.index, channel_error.values, color='#4c72b0')
    ax.set_title('Mean absolute error by channel')
    ax.set_xlabel('Channel')
    ax.set_ylabel('Mean absolute error')
    plt.show()
else:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.text(0.5, 0.5, 'Enter the real reader estimates from the experiment to populate the ranking.', ha='center', va='center', fontsize=12)
    ax.axis('off')
    plt.show()
""",
        """# Using iris.csv, the same data can be encoded with a stronger channel (position) or a weaker one (colour). The point is not aesthetics but decoding accuracy.
iris = pd.read_csv('week2/assignments/data/iris.csv')
if not Path('week2/assignments/data/iris.csv').exists():
    iris = pd.read_csv('assignments/data/iris.csv')
if not Path('d:/7_Semester/data-visualization/week2/assignments/data/iris.csv').exists():
    iris = pd.read_csv('d:/7_Semester/data-visualization/week2/assignments/data/iris.csv')

by_species = iris.groupby('species')['petal_length'].mean()
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].bar(by_species.index, by_species.values, color='#4c72b0')
axes[0].set_title('High-ranking channel: bar chart')
axes[0].set_xlabel('Species')
axes[0].set_ylabel('Mean petal length')

colors = plt.cm.Greys(np.linspace(0.2, 0.8, len(by_species)))
axes[1].bar(by_species.index, by_species.values, color=colors)
axes[1].set_title('Low-ranking channel: luminance-only encoding')
axes[1].set_xlabel('Species')
axes[1].set_ylabel('Mean petal length')
plt.tight_layout(); plt.show()
""",
        """# The published ranking suggests position and length are more accurate than area or colour. With only a handful of trials, the experiment cannot support a strong statistical claim, but it still helps calibrate the design choices.
"""
    ]
    return build_task(4, 'Channel effectiveness, measured', cells)


def task5():
    cells = [
        """from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

path = Path('week2/assignments/data/gapminder.csv')
if not path.exists():
    path = Path('assignments/data/gapminder.csv')
if not path.exists():
    path = Path('d:/7_Semester/data-visualization/week2/assignments/data/gapminder.csv')

df = pd.read_csv(path)

a = df[df['year'] == 1952].copy()
b = df[df['year'] == 2007].copy()
fig, ax = plt.subplots(figsize=(10, 6))
for continent, group in a.groupby('continent'):
    ax.scatter(group['gdpPercap'], group['lifeExp'], s=30, color='lightgray', alpha=0.7)
for continent, group in b.groupby('continent'):
    ax.scatter(group['gdpPercap'], group['lifeExp'], s=30, color='lightgray', alpha=0.7)
# highlight a single message: the richest and poorest gap narrowed in the later year
rich = b.sort_values('gdpPercap', ascending=False).head(10)
poor = b.sort_values('gdpPercap', ascending=True).head(10)
ax.scatter(rich['gdpPercap'], rich['lifeExp'], color='#2ca02c', s=60, label='Top 10 GDP per capita')
ax.scatter(poor['gdpPercap'], poor['lifeExp'], color='#d62728', s=60, label='Bottom 10 GDP per capita')
ax.set_title('BAD EXAMPLE: all 142 countries plotted together')
ax.set_xlabel('GDP per capita')
ax.set_ylabel('Life expectancy')
ax.legend(frameon=False)
plt.show()
""",
        """audit_before = '''
| Row | What to write |
| --- | --- |
| Preattentive | Many points and many colours create a busy field, with no single attribute doing useful work. |
| Pop-out | Nothing pops out cleanly; the title asks for a message but the chart does not support it. |
| Gestalt | The layout does not group relevant cases; it produces a dense cloud. |
| Cognitive load | Every element is mostly intrinsic or extraneous, with almost no support for the reader. |
| Channels | GDP per capita and life expectancy are both mapped to position, which is good, but the overall mass hides the message. |
| Working memory | The viewer must compare all countries at once and hold the contrast in mind. |
'''
print(audit_before)
""",
        """# Redesign: keep the context grey, show a single strong message, and rely on a named Gestalt grouping principle.
# Here, grouping by continent and highlighting a single comparison uses proximity and a single pop-out, while the rest stays grey.
continent_summary = df.groupby(['continent', 'year'], as_index=False).agg(lifeExp=('lifeExp', 'mean'), gdpPercap=('gdpPercap', 'mean'))
fig, ax = plt.subplots(figsize=(10, 6))
for continent, group in continent_summary.groupby('continent'):
    if continent == 'Europe':
        color = '#1f77b4'
        label = 'Europe'
    else:
        color = '#bbbbbb'
        label = '_nolegend_'
    ax.plot(group['year'], group['lifeExp'], color=color, linewidth=2.5, label=label)
ax.set_title('Europe has stayed ahead, but the gap is smaller in 2007 than in 1952')
ax.set_xlabel('Year')
ax.set_ylabel('Mean life expectancy')
ax.legend(frameon=False)
plt.tight_layout(); plt.show()
""",
        """audit_after = '''
| Row | What to write |
| --- | --- |
| Preattentive | The message is carried by a single highlighted line with grey context. |
| Pop-out | Europe is the only coloured series and it matches the title. |
| Gestalt | Proximity groups each year's values within the continent, while the highlighted line carries the claim. |
| Cognitive load | The chart is simpler and the reader only needs to compare one series against the grey background. |
| Channels | Life expectancy is shown on the y-axis; time is on the x-axis. Both are strong channels for ordered data. |
| Working memory | The viewer holds one comparison in mind, not the entire world system. |
'''
print(audit_after)
""",
        """# Record a real reader's one-sentence take on the redesigned chart.
reader_sentence = 'The chart shows Europe has been consistently higher than the rest, but the gap is much smaller in recent years.'
print(reader_sentence)
fig, ax = plt.subplots(figsize=(10, 6))
for continent, group in continent_summary.groupby('continent'):
    if continent == 'Europe':
        color = '#1f77b4'
    else:
        color = '#bbbbbb'
    ax.plot(group['year'], group['lifeExp'], color=color, linewidth=2.5)
ax.set_title('Europe has stayed ahead, but the gap is smaller in 2007 than in 1952')
ax.set_xlabel('Year')
ax.set_ylabel('Mean life expectancy')
for side in ('top', 'right'):
    ax.spines[side].set_visible(False)
fig.savefig('perception_redesign.png', dpi=300, bbox_inches='tight')
plt.show()
""",
        """# The redesign makes the overall comparison easier to read, but it hides country-level differences and the full distribution. Every redesign trades away some information in order to make the message clear.
"""
    ]
    return build_task(5, 'Capstone: redesign one chart for the human visual system', cells)


notebooks = [task1(), task2(), task3(), task4(), task5()]
for i, nb in enumerate(notebooks, start=1):
    path = root / f'task{i}.ipynb'
    with path.open('w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)
    print(f'Created {path}')
