# Week 3 Graph Analysis

## Purpose and scope

This report explains the Week 3 figures and statistical summaries: what each visual suggests, what the data support, why the misleading versions fail, and what the redesigned views clarify. The nine Part A datasets and the clinical review data are synthetic, generated for CDB601220; their scenarios are illustrative, not real clinical or operational evidence.

The central lesson is that a chart can be numerically accurate and still invite an unsupported conclusion. Aggregation, changing coverage, outliers, arbitrary binning, smoothing, and inconsistent visual scales can all change the story a reader sees. A redesign should expose the data structure and uncertainty rather than merely make the chart look cleaner.

## Part A: Nine chart diagnoses


### 1. Helmet grade and injury rates

The aggregate bar chart invites the conclusion that premium helmets are riskier: the rate is 5.40 head injuries per 1,000 trips for Premium versus 2.15 for Standard, about 2.51 times as high. The chart correctly calculates those overall rates, but it combines very different trip mixes. About 85% of Premium trips are on motorways, compared with only 3.3% of Standard trips. Motorway exposure has a higher injury rate. Once rates are compared within road type, Premium is lower in all three groups: 6.00 versus 8.00 on motorways, 2.20 versus 3.00 on city arterials, and 1.00 versus 1.39 in inner-city lanes. This is a Simpson's paradox caused by differing group composition. Premium riders also average 67.0 kph versus 30.2 kph, so helmet grade is entangled with rider behaviour. The stratified chart is more informative, but these observational data do not establish a causal helmet effect.

### 2. Chai sales and quiz failures

The monthly scatterplot gives a strong positive raw-count correlation, $r=0.982$, and can make chai sales seem predictive of quiz failures. Both counts also rise with enrollment: enrollment increases from 1,765 to 5,406 students, and correlates with chai sales at $r=0.997$ and failures at $r=0.977$. Enrollment is a shared exposure that explains much of the apparent association. After expressing both measures per 1,000 students, their correlation is $r=0.293$; the partial correlation after linearly controlling for enrollment is $r=0.455$. Exam timing remains context: mean failures per 1,000 students are 38.62 in exam months and 34.15 otherwise. The normalized time-series panels remove the raw population-size effect, but neither normalization nor partial correlation proves that chai has no relationship with performance or that exams are the only remaining explanation.

### 3. AQI before and after the action plan

The all-row calculation reproduces the apparent fall from mean AQI 202.09 in days 1–60 to 137.21 in days 61–120, approximately 32%. The second panel reveals the key mechanism: coverage changes from 22 reporting stations per day to 13, and all six Industrial stations stop reporting after day 60. The means therefore compare different station mixtures. Restricting both periods to the same 13 stations produces 137.09 before and 137.21 after, effectively no change in this synthetic series. The same-station chart controls the coverage mix and does not support a claim that the action plan reduced AQI. It cannot by itself establish what caused air quality to change.

### 4. Department averages hide individual structure

All four departments have the same reported summary to rounding: $n=11$, mean study time 18.00 hours, mean score 14.50/20, correlation about 0.816, and slope about 0.25 score points per hour. The scatterplots show why the table is inadequate. In Architecture, ten students report exactly 16 study hours; one observation at 38 hours and a score of 19.50 supplies all the variation in study hours. For those ten students, the standard deviation of hours is zero, so their within-group correlation is undefined. Electrical Engineering also includes a high score of 19.74 at 26 hours. The plotted points reveal leverage and distribution differences concealed by matching summaries. Equal averages are not evidence that departments have identical student experiences or should automatically receive equal funding.

### 5. Identical statistics, different shapes

The five cohorts each have $n=180$, mean platform time 48, mean score 63, population standard deviations 12 and 15, and Pearson $r=0.420$. Their scatterplots nevertheless form a noisy straight trend, a ring, a star, two clusters, and an X. Means, standard deviations, and a single linear correlation do not describe nonlinear structure, subgroups, or the geometry of the observations. The common-axis small multiples expose those differences; the summary table remains useful but cannot stand in for looking at the data.

### 6. Correlation heatmap and biomarker claim

The original 20-by-20 matrix reproduces creatinine–HbA1c $r=0.765$ and systolic–MAP $r=0.958$. The first value is a pooled association, not proof of a diagnostic relationship. It varies sharply by site: the correlation is -0.114 at Site D, -0.049 at Site A, and 0.918 at Site C. A pooled result hides this heterogeneity. The matrix also contains six unassigned instrument probes; correlations involving them lack a calibrated physical interpretation and should not be treated as meaningful measurements without instrument documentation.

There is also a visual encoding problem. Sequential Reds with automatic limits has no neutral midpoint for negative correlations, so colour does not consistently communicate sign or comparable magnitude. Displaying both triangles duplicates every pair. The redesign uses a diverging scale fixed to -1 through +1, centers it at zero, and masks the upper triangle. These changes make the correlation display more faithful, but they do not resolve site variation, multiplicity across 190 pairs, unassigned probes, or the distinction between association and causation. The very high systolic–MAP value is partly arithmetic because MAP is derived from systolic and diastolic pressure.

### 7. Revenue and cost on dual axes

The dual-axis figure makes cost appear above revenue for January through April because its two y-axes use independently selected ranges (50–80 and 40–56), despite both measures using PKR millions. This is a visual ordering created by the axis transformations, not a loss in the data. On a shared scale, revenue exceeds cost in every month; the margins are +8, +12, +14, +17, +20, and +25 million PKR from January to June. A dual-axis chart has no single shared visual scale from which to calculate a meaningful Lie Factor. The shared-axis redesign communicates the actual comparison directly.

### 8. Histogram bin counts

Each histogram contains the same 10,000 systolic readings. Three bins merge the two broad clusters into a coarse summary; 45 bins show more detail; 400 bins make random local count changes look like meaningful structure. Bin count changes the visual impression, not the observations. The Freedman–Diaconis rule gives a reproducible data-adaptive choice here: 29 bins with a mean width of 3.69 mmHg. This is a defensible view of the broad shape, not a uniquely true histogram; the parameter should be reported and readers should understand that different binning can change apparent detail.

### 9. SpO2 density beyond the physical ceiling

The observed SpO2 data have a maximum of 100%, no observations above 100%, and 304 records exactly at 100%. A Gaussian kernel density estimate uses smooth, unbounded kernels; smoothing observations at the 100% boundary therefore draws an artificial tail above the physical maximum. With Scott's bandwidth, `bw_adjust=1`, and `cut=3`, the tail is 1.551% of the estimated density area. That is not the percentage of patients above 100%; the observed percentage is zero. The requested 4.4% claim is not reproduced by this stated KDE configuration. A count plot of the observed integer values preserves the discrete data and physical ceiling.

## Part B: Lie Factor audit

The Lie Factor compares the proportional change encoded by the graphic with the proportional change in the data. A value near 1 is faithful; the assignment's tolerance is 0.95–1.05.

| Chart | Lie Factor | Interpretation |
|---|---:|---|
| A | 75.00 | Strong exaggeration: the visible bar segment is measured from a truncated baseline. |
| B | 2.50 | Exaggeration: a coin is enlarged in both height and width, so its area grows quadratically. |
| C | 1.00 | Honest: the zero-based bar length tracks the 25-to-30 data increase. |
| D | 0.25 | Understatement: the data rise 50%, while the bar ink grows only 12.5%. |
| E | 5.00 | Exaggeration: bubble area grows with the square of its radius. |

Chart C is the only honest measured graphic. Charts B and E require `ink_dimension=2`: Chart B's 1.5-times linear scaling makes 2.25-times the area, and Chart E's four-times radius makes 16-times the area. Treating either as a length incorrectly makes the distortion disappear in the calculation. Chart D is still misleading even though it understates the change; a reader could be less concerned about worsening AQI. The measurements do not identify who made the graphic or who intended to benefit.

Chart F, the dual-axis revenue/cost display, has no meaningful single Lie Factor because the two series use separate scales and there is no one encoded effect to compare against one data effect. The underlying six monthly margins remain positive and increase from PKR 8 million to PKR 25 million.

## Part C: Palette and accessibility figure

The swatch sheet compares the first four Matplotlib `tab10` colours with the course palette plus its fourth slot under normal vision and Machado severity-1.0 deutan, protan, and tritan simulations. The colours are tested pairwise in OKLab rather than declared safe by appearance alone.

The four-colour `tab10` selection fails under deutan (S3/S4, ΔE 4.06) and protan (S2/S3, ΔE 0.68), both below the toolkit's failure threshold of 6. Under tritan, its closest pair is S1/S3 at ΔE 6.72, which needs another distinguishing channel. The course palette's closest pair with the fourth hue is S3 `#009E73` and S4 `#CC79A7` under deutan, ΔE 7.55. This is below the target of 8: the fourth hue must not identify a category by itself. The practical rule is to use no more than the three audited course hues as the sole category signal; beyond that, add direct labels, marker shapes, line styles, a table, or small multiples. The fourth hue also needs direct labels or a table.

## Part D: Clinical review figure

The 2×2 review figure screens the synthetic cohort; it is not a causal model or a clinical decision tool.

1. **Systolic-pressure histogram.** The distribution has two broad clusters. The figure uses 29 Freedman–Diaconis bins, averaging 3.69 mmHg in width, and labels the number of plotted records. A histogram is appropriate for a numeric distribution and avoids the false precision of excessive bins.
2. **Length-of-stay box plot.** The ward medians differ and all groups have a long upper tail. The plot orders wards by median stay, retains fliers, and uses a symmetric-log axis so zero-day stays and the long tail can both be seen. There are two zero-day records and the maximum stay is 273.65 days. The log-like scale must be read with care; vertical distances are not linear in days.
3. **Systolic/diastolic scatter.** These measures move together strongly ($r=0.889$, $n=9,971$). Shared quantitative position is appropriate for comparing two numeric measurements. Correlation does not show that one pressure causes the other, and the association may partly reflect their shared physiology.
4. **Correlation heatmap.** The 9-by-9 Pearson matrix summarizes signed associations among nine measured variables. MAP is excluded because it is calculated from systolic and diastolic pressure. The diverging `RdBu_r` palette is pinned to -1…+1, centered at zero, annotated, and shown once per pair by masking the upper triangle. Correlations summarize linear association and are not causal effects.

### Data cleaning and ethical reporting


The review begins with 10,000 records. Twelve ward spellings are normalized into four canonical ward names, removing no rows. Admission dates from three export formats are parsed explicitly; all dates parse and no rows are removed. BMI sentinel values are recoded as missing rather than deleted: 84 zeros and 402 values of 999, or 486 cells total. The BMI mean changes from 66.18 to 27.35 kg/m² after that correction.

Twenty-nine heart-rate readings above 250 bpm are excluded as device faults, leaving 9,971 records. Mean heart rate changes from 78.8331 to 77.9843 bpm. The report includes both the filtered figure and the unfiltered appendix figure so the exclusion is visible and auditable. The threshold is a stated measurement-quality rule, not a choice made to strengthen a chart. No other rows are removed, and BMI sentinel cells are not counted as removed rows.

## Bonus: Preattentive search figure

The four panels use the same 12-by-18 synthetic digit grid, the same nine target 3s, and identical target positions. They compare no pop-out, colour only, size only, and redundant colour-plus-shape. This controls the stimulus while changing the visual channel. The panel illustrates how a salient colour or size difference can guide attention, and how redundant cues can support detection when colour is not available. The generated panel is not a timing result: timing and accuracy results require five real classmates and 20 recorded trials. Until those observations are entered, no channel can honestly be called fastest or slowest.

## Overall conclusions

Across these examples, the strongest analyses are the ones that expose the mechanism: stratifying helmet rates by road type, adjusting shared counts for enrollment, holding AQI station composition constant, inspecting points behind summary statistics, checking site-specific correlations, and using common axes for direct comparisons. Visual design also needs statistical discipline: declare binning and smoothing parameters, respect physical bounds, show signed correlations on a fixed diverging scale, and disclose exclusions. The redesigned charts improve interpretation, but none turns synthetic or observational data into causal evidence.

## Sources and reproducibility

- [Week 3 assignment brief](assignments/TASKS.md)
- [Data dictionary](assignments/data/DATA_DICTIONARY.md)
- [Part A analysis and figures](task1.ipynb)
- [Lie Factor analysis](taskb.ipynb)
- [Palette audit](taskc.ipynb)
- [Clinical review and written justification](taske.ipynb)
- [Bonus pop-out experiment](bones.ipynb)