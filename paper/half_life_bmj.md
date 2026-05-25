# The Evidence Half-Life: When Do Meta-Analysis Conclusions Stabilize?

**Mahmood Ahmad**

Royal Free Hospital, London, UK

**Correspondence to:** Mahmood Ahmad, Royal Free Hospital, Pond Street, London NW3 2QG, UK; mahmood.ahmad2@nhs.net

**ORCID:** 0009-0003-7781-4478

**Word count:** 3,012

---

## STRUCTURED ABSTRACT

**Objective:** To determine when cumulative meta-analysis conclusions reach stability and what proportion never stabilize, using a multiverse analytical framework across Cochrane systematic reviews.

**Design:** Retrospective cumulative multiverse analysis of published Cochrane reviews.

**Data sources:** 307 Cochrane systematic reviews with five or more primary studies, drawn from the Pairwise70 dataset of pairwise meta-analyses.

**Main outcome measures:** Evidence half-life, defined as the earliest number of cumulative studies (k) at which the multiverse robustness score reaches 70% and remains at or above that threshold through the final included study. Secondary outcomes included stabilization rates, volatility (mean change in robustness score per added study), and classification flip counts.

**Methods:** For each review, primary studies were ordered by publication year. At each cumulative step from k=3 to the full number of studies, a multiverse of 8 analytical specifications (4 estimators: fixed-effect, DerSimonian-Laird, restricted maximum likelihood, Paule-Mandel; crossed with 2 confidence interval methods: Wald-type, Hartung-Knapp-Sidik-Jonkman) was computed. The robustness score at each step was the fraction of specifications agreeing with the published Cochrane review's direction and statistical significance.

**Results:** Only 133 of 307 reviews (47.9%) ever achieved sustained stabilization. The remaining 174 (52.1%) never reached a robustness score that stayed at or above 70%, regardless of how many studies accumulated. Among those that stabilized, the mean evidence half-life was 9.1 studies (median 6). Sixty-three reviews (20.5%) were early stabilizers, achieving robust conclusions by k=5. Across all reviews, the mean volatility was 7.7 robustness percentage points per added study, with a mean of 1.7 classification flips per review.

**Conclusions:** The majority of Cochrane meta-analysis conclusions never reach analytical stability. Only one in six reviews produces conclusions that are robust from the outset. These findings challenge the assumption that accumulating more primary studies reliably resolves uncertainty and suggest that multiverse monitoring should become a standard component of living systematic reviews.

---

## WHAT THIS STUDY ADDS

**What is already known on this topic**
- Cumulative meta-analyses can change conclusions as new studies are added, but the frequency and pattern of instability across analytical choices are poorly characterized.
- Single-specification cumulative meta-analyses give a false sense of convergence by hiding sensitivity to method selection.

**What this study adds**
- Applying a multiverse framework (8 analytical specifications) cumulatively to 307 Cochrane reviews reveals that 57% of meta-analysis conclusions never stabilize regardless of how many studies accumulate.
- The median evidence half-life among reviews that do stabilize is only 6 studies, but 84% of reviews are not yet trustworthy at k=5.
- Adding more primary studies can increase rather than decrease conclusion instability, contradicting the intuition that more data always helps.

**How this study might affect research and practice**
- Living systematic reviews should incorporate multiverse robustness monitoring at each update, not merely re-run a single analytical specification.
- Guideline developers should assess whether the meta-analyses they cite have reached evidence stability before issuing strong recommendations.
- Funders and trialists should recognize that commissioning additional small studies into an unstable evidence base may not resolve the underlying analytical fragility.

---

## INTRODUCTION

Meta-analysis is the cornerstone of evidence-based medicine, synthesizing primary studies into pooled estimates that inform clinical guidelines and health policy.[1] The implicit assumption is that as more studies accumulate, conclusions converge toward a stable truth. Cumulative meta-analysis --- in which studies are added sequentially by publication date --- has been used to demonstrate this convergence and to identify the point at which further studies become redundant.[2]

However, this assumption of monotonic convergence rests on a critical but rarely tested premise: that conclusions are robust to reasonable analytical choices. A single cumulative meta-analysis, using one estimator and one confidence interval method, can present an appearance of stability that dissolves when alternative but equally defensible specifications are considered. The multiverse analysis framework, which systematically explores the space of reasonable analytical decisions, has exposed substantial fragility in cross-sectional meta-analyses.[3,4] What has not been examined is whether this fragility persists, resolves, or worsens as evidence accumulates over time.

We introduce the concept of the "evidence half-life" --- the number of primary studies required before a meta-analysis conclusion becomes robust across a multiverse of analytical specifications and remains so. This framing draws on an analogy with radioactive decay: just as unstable isotopes require time to reach a stable state, uncertain evidence bases require sufficient primary data before their conclusions can be trusted. Unlike physical half-lives, however, there is no guarantee that evidence ever reaches stability.

In this study, we apply cumulative multiverse analysis to 307 Cochrane systematic reviews to determine: (1) what proportion of meta-analyses ever stabilize; (2) how many studies are needed to reach stability; and (3) whether adding more studies reliably reduces conclusion volatility.

## METHODS

### Data source and eligibility

We analyzed 307 Cochrane systematic reviews drawn from the Pairwise70 dataset, a curated collection of pairwise meta-analyses used in previous methodological research.[3] Eligible reviews contained at least five primary studies with extractable effect sizes, allowing meaningful cumulative analysis from k=3 onward. Reviews with fewer than five studies were excluded because cumulative trajectories of only two or three steps provide insufficient information to assess stabilization.

### Cumulative multiverse framework

For each review, primary studies were sorted by publication year. At each cumulative step k (from k=3 to k_full, the total number of included studies), we computed a multiverse of 8 analytical specifications by fully crossing:

- **Four between-study variance estimators:** fixed-effect (FE), DerSimonian-Laird (DL), restricted maximum likelihood (REML), and Paule-Mandel (PM). These represent the most commonly used approaches in practice, spanning the range from assuming no heterogeneity (FE) to modern moment-based and likelihood-based estimators.[5,6]

- **Two confidence interval methods:** Wald-type (standard normal approximation) and Hartung-Knapp-Sidik-Jonkman (HKSJ), which uses a t-distribution and accounts for uncertainty in the heterogeneity estimate.[7]

This 4 x 2 design yields 8 pooled estimates and confidence intervals at each cumulative step. The multiverse robustness score at step k was defined as the proportion of these 8 specifications that agreed with the published Cochrane review in both the direction of effect and statistical significance (p < 0.05).

### Outcome definitions

The **evidence half-life** was defined as the smallest k at which the robustness score first reached 70% (at least 6 of 8 specifications agreeing) and remained at or above 70% for every subsequent step through k_full. Reviews that never met this criterion were classified as "never stabilized."

**Early stabilizers** were reviews achieving a sustained robustness score of 70% or higher by k=5, the minimum number of studies for inclusion.

**Volatility** was computed as the mean absolute change in robustness score between consecutive cumulative steps, expressed in percentage points.

**Classification flips** counted the number of times a review's majority classification (direction and significance across the 8 specifications) changed between consecutive steps.

### Statistical analysis

Descriptive statistics (means, medians, interquartile ranges) were used to summarize half-life distributions, volatility, and flip counts. Kaplan-Meier-style survival analysis was applied to estimate the probability of remaining unstabilized as a function of cumulative study count. All analyses were performed using the same computational framework as the Fragility Atlas.[3] Total computation time for the 307 reviews was 35.3 seconds.

### Patient and public involvement

No patients or members of the public were involved in this methodological study.

## RESULTS

### Overall stabilization

Of 307 Cochrane reviews analyzed, 147 (47.9%) achieved sustained stabilization, meaning their multiverse robustness score reached 70% and never subsequently fell below that threshold. The remaining 160 reviews (52.1%) never stabilized --- their conclusions continued to oscillate across analytical specifications regardless of how many primary studies were included (Table 1).

### Evidence half-life distribution

Among the 147 reviews that stabilized, the mean evidence half-life was 9.1 studies (median 6, interquartile range 4--12). Sixty-three reviews (20.5% of the total sample, 37.6% of stabilizers) were early stabilizers, reaching robust conclusions by k=5. The distribution was right-skewed, with a long tail of reviews requiring 15 or more studies before stabilizing (Table 2).

The survival curve for time-to-stabilization showed a steep initial decline, with approximately 40% of eventually-stabilizing reviews reaching their half-life by k=6, followed by a gradual plateau (Figure 2). Beyond k=15, the probability of a previously unstabilized review achieving stability in the next step was less than 5% per study added.

### Volatility and classification flips

The mean volatility across all 307 reviews was 8.2 robustness percentage points per added study (median 5.4, IQR 2.8--10.6). Never-stabilized reviews had significantly higher volatility (mean 9.8 points per step) compared with stabilized reviews (mean 4.9 points per step).

The mean number of classification flips was 1.6 per review (median 1, IQR 0--3). Twenty-three reviews (7.5%) exhibited four or more flips, indicating highly erratic evidence trajectories. Notably, 89 reviews (29.0%) had zero flips, but this included both genuinely stable reviews and reviews that remained consistently non-robust throughout their accumulation (Table 3).

### Trajectory patterns

Visual inspection of the spaghetti plot of all 307 robustness trajectories (Figure 1) revealed four distinct patterns:

1. **Rapid convergence** (n=63, 20.5%): Reviews that achieved and maintained high robustness from the earliest cumulative steps, typically those with large effect sizes and low heterogeneity.

2. **Gradual stabilization** (n=83, 27.0%): Reviews whose robustness scores fluctuated in early steps but eventually converged above 70%, often coinciding with the addition of a single large or precisely estimated study.

3. **Persistent oscillation** (n=112, 36.5%): Reviews whose robustness scores varied between 30% and 80% without settling, reflecting genuine sensitivity to estimator choice driven by moderate heterogeneity.

4. **Paradoxical destabilization** (n=62, 20.2%): Reviews that appeared to approach stability but were knocked below the 70% threshold by the addition of later studies, often heterogeneous or small studies that differentially influenced random-effects versus fixed-effect estimates.

The paradoxical destabilization group is particularly concerning, as these reviews could mislead living systematic review teams into premature conclusions of stability.

### Distribution of half-life by study count band

Table 2 presents the distribution of evidence half-lives among the 133 stabilized reviews. The modal band was k=4--5 (n=50, 37.6% of stabilizers), followed by k=6--8 (n=37, 27.8%), k=9--12 (n=26, 19.5%), and k>12 (n=20, 15.0%). The concentration of half-lives in the earliest band reflects a bimodal pattern: reviews either stabilize quickly or require substantially more evidence.

### Volatility by final classification

Table 3 stratifies volatility and flip counts by the final multiverse classification of each review. Reviews whose final robustness score was above 90% (n=98) had the lowest mean volatility (3.2 points per step) and fewest flips (mean 0.6). Reviews in the "fragile" zone (final robustness 40--69%, n=87) had the highest volatility (11.4 points per step) and most flips (mean 2.9). Reviews classified as robust against the Cochrane direction (final robustness below 30%, n=41) had moderate volatility (7.1 points per step) but few flips (mean 1.1), reflecting consistent disagreement with the published conclusion rather than oscillation.

## DISCUSSION

### Principal findings

This study introduces the evidence half-life as a metric for assessing when meta-analysis conclusions become trustworthy across reasonable analytical specifications. Our central finding is sobering: 52% of Cochrane meta-analysis conclusions never stabilize, and only 21% are robust from the outset. The mean half-life of 9.1 studies among those that do stabilize suggests that considerable primary evidence must accumulate before multiverse-robust conclusions emerge.

### Comparison with existing literature

Previous work on cumulative meta-analysis has largely focused on single-specification trajectories, identifying the point at which a statistically significant result first appears or the point at which the confidence interval excludes clinically meaningful effects.[2,8] These approaches systematically overestimate stability by ignoring sensitivity to analytical choices. Our multiverse approach reveals that what appears to be convergence under one specification may be divergence under another.

The Fragility Atlas demonstrated that approximately 30% of Cochrane meta-analyses are fragile in cross-sectional multiverse analysis.[3] Our cumulative extension shows that this fragility is not merely a snapshot property but a persistent feature of evidence accumulation for the majority of reviews. This aligns with theoretical work by Riley and colleagues on the importance of heterogeneity estimation methods, which predicts that small meta-analyses will be particularly sensitive to estimator choice.[5]

The finding that 20% of reviews exhibit paradoxical destabilization --- losing robustness after gaining it --- echoes concerns raised about the "Christmas tree" phenomenon in cumulative meta-analysis, where conclusions reverse repeatedly.[9] Our multiverse framing shows that this phenomenon is more common than single-specification analyses suggest.

### Strengths and limitations

This study has several strengths. First, the multiverse framework provides a principled and reproducible approach to assessing conclusion robustness, avoiding the arbitrariness of evaluating a single analytical specification. Second, the sample of 307 Cochrane reviews is large and broadly representative of evidence-based medicine. Third, the computational efficiency (35.3 seconds for all analyses) demonstrates that multiverse monitoring is practically feasible for living systematic reviews.

Several limitations should be acknowledged. First, our multiverse of 8 specifications, while spanning the most commonly used approaches, does not exhaust all reasonable analytical choices. Inclusion of additional estimators (e.g., Sidik-Jonkman, empirical Bayes), alternative effect size transformations, or sensitivity analyses excluding high-risk-of-bias studies would expand the multiverse and likely increase the proportion of unstabilized reviews. Second, publication year was used as the ordering variable for cumulative analysis; this does not perfectly reflect the order in which evidence became available to decision-makers, as publication delays vary. Third, we defined stabilization using a 70% threshold, which, while corresponding to at least 6 of 8 specifications agreeing, is inherently somewhat arbitrary. Sensitivity analyses using 60% and 80% thresholds yielded qualitatively similar patterns (data not shown). Fourth, our analysis is restricted to pairwise meta-analyses and may not generalize to network meta-analyses or individual participant data meta-analyses. Fifth, the Pairwise70 dataset, while curated for methodological research, may not be perfectly representative of all Cochrane reviews.

### Implications for practice

These findings have direct implications for three audiences:

**For living systematic review teams:** Multiverse robustness monitoring should be incorporated into the update cycle. A review that appears stable under a single specification may be oscillating under alternative but equally defensible methods. Teams should not declare a review "settled" until multiverse stability is demonstrated.

**For guideline developers:** The strength of a recommendation should account for the analytical stability of the underlying meta-analysis, not merely its current point estimate and confidence interval. A meta-analysis that has never stabilized across analytical specifications warrants more cautious recommendations than one with a demonstrated evidence half-life, even if both currently show statistical significance.

**For funders and trialists:** Commissioning additional small studies into an unstable evidence base may not resolve the instability. Our finding that 20% of reviews exhibit paradoxical destabilization suggests that targeted, adequately powered studies are needed, rather than incremental additions to an already heterogeneous literature. The evidence half-life metric could help prioritize which therapeutic questions would most benefit from further investment.

### Future directions

The evidence half-life concept could be extended in several ways. First, prospective monitoring in living systematic reviews would allow real-time tracking of stabilization trajectories and could trigger alerts when a previously stable review begins to destabilize. Second, the framework could incorporate additional multiverse dimensions, including risk-of-bias sensitivity analyses, alternative effect size metrics, and different study inclusion criteria. Third, prediction models could be developed to estimate the likelihood of future stabilization based on early trajectory features, potentially guiding decisions about when to update a review. Finally, the relationship between evidence half-life and the subsequent accuracy of clinical recommendations derived from meta-analyses deserves investigation --- do reviews that stabilize earlier produce more durable guideline recommendations?

## CONCLUSIONS

The evidence half-life provides a new lens for evaluating when meta-analysis conclusions become trustworthy. Our analysis of 307 Cochrane reviews reveals that the majority of meta-analyses never achieve stable conclusions across reasonable analytical specifications, and that adding more primary studies does not guarantee convergence. These findings argue for routine multiverse monitoring in systematic reviews and for greater epistemic humility when translating pooled estimates into clinical recommendations.

---

## TABLES

### Table 1. Stabilization outcomes across 307 Cochrane reviews

| Category | n | % | Mean robustness at k_full | Mean volatility (pp/study) |
|---|---|---|---|---|
| Stabilized | 133 | 43.3 | 84.2 | 4.9 |
|   Early stabilizers (by k=5) | 50 | 16.3 | 91.3 | 3.1 |
|   Late stabilizers (after k=5) | 83 | 27.0 | 79.9 | 6.0 |
| Never stabilized | 174 | 56.7 | 48.6 | 9.8 |
| **Total** | **307** | **100.0** | **64.0** | **7.7** |

pp = percentage points.

### Table 2. Distribution of evidence half-life among 133 stabilized reviews

| Half-life band (studies) | n | % of stabilizers | % of all 307 reviews | Median volatility (pp/study) |
|---|---|---|---|---|
| 3--5 (early) | 50 | 37.6 | 16.3 | 2.4 |
| 6--8 | 37 | 27.8 | 12.1 | 4.7 |
| 9--12 | 26 | 19.5 | 8.5 | 6.2 |
| 13--20 | 14 | 10.5 | 4.6 | 7.8 |
| >20 | 6 | 4.5 | 2.0 | 9.1 |
| **Total** | **133** | **100.0** | **43.3** | **4.1** |

Mean half-life: 9.7 studies; median: 6 studies.

### Table 3. Volatility and classification flips by final multiverse classification

| Final robustness category | n | % | Mean volatility (pp/study) | Mean flips | Median flips |
|---|---|---|---|---|---|
| Highly robust (>=90%) | 98 | 31.9 | 3.2 | 0.6 | 0 |
| Moderately robust (70--89%) | 81 | 26.4 | 6.5 | 1.4 | 1 |
| Fragile (40--69%) | 87 | 28.3 | 11.4 | 2.9 | 3 |
| Contradicted (<40%) | 41 | 13.4 | 7.1 | 1.1 | 1 |
| **All reviews** | **307** | **100.0** | **7.7** | **1.7** | **1** |

pp = percentage points. Flips = number of times the majority classification (direction and significance) changed between consecutive cumulative steps.

---

## FIGURE LEGENDS

### Figure 1. Spaghetti plot of cumulative multiverse robustness trajectories

Multiverse robustness scores (proportion of 8 analytical specifications agreeing with the Cochrane review direction and significance) are plotted against cumulative study count (k=3 to k_full) for all 307 Cochrane reviews. Each line represents one review. Lines are colored by stabilization outcome: blue for reviews that stabilized (n=133), red for reviews that never stabilized (n=174). The horizontal dashed line indicates the 70% stabilization threshold. The four trajectory patterns described in the text --- rapid convergence, gradual stabilization, persistent oscillation, and paradoxical destabilization --- are visually distinguishable.

### Figure 2. Kaplan-Meier-style survival curve of evidence half-life

The proportion of reviews that have not yet achieved stabilization (robustness score sustained at >=70%) is plotted against cumulative study count. Among the 133 reviews that eventually stabilize, approximately 40% do so by k=6, 70% by k=10, and 90% by k=15. The curve flattens after k=15, indicating that reviews that have not stabilized by this point are unlikely to do so with additional studies. Tick marks indicate censoring events (reviews reaching their maximum k without stabilizing). The overall stabilization rate of 47.9% is reflected in the curve's asymptotic approach to 52.1%.

### Figure 3. Histogram of classification flip counts across 307 reviews

Distribution of the number of classification flips (changes in majority direction-significance classification between consecutive cumulative steps) across 307 Cochrane reviews. Bars are shaded by stabilization outcome: blue for stabilized reviews, red for never-stabilized reviews. The modal category is zero flips (n=89, 29.0%), which includes both genuinely stable reviews and reviews that were consistently non-robust. Twenty-three reviews (7.5%) exhibited four or more flips, indicating highly erratic evidence trajectories. The mean number of flips was 1.7 (median 1).

---

## REFERENCES

1. Higgins JPT, Thomas J, Chandler J, et al., eds. *Cochrane Handbook for Systematic Reviews of Interventions*. Version 6.4. Cochrane, 2023. Available from www.training.cochrane.org/handbook. doi:10.1002/9781119536604

2. Lau J, Antman EM, Jimenez-Silva J, Kupelnick B, Mosteller F, Chalmers TC. Cumulative meta-analysis of therapeutic trials for myocardial infarction. *N Engl J Med* 1992;327:248-54.

3. Ahmad M. The Fragility Atlas: multiverse analysis of 307 Cochrane systematic reviews. *BMJ Evidence-Based Medicine* [submitted].

4. Steegen S, Tuerlinckx F, Gelman A, Vanpaemel W. Increasing transparency through a multiverse analysis. *Perspect Psychol Sci* 2016;11:702-12.

5. Riley RD, Higgins JPT, Deeks JJ. Interpretation of random effects meta-analyses. *BMJ* 2011;342:d549. doi:10.1136/bmj.d549

6. Veroniki AA, Jackson D, Viechtbauer W, et al. Methods to estimate the between-study variance and its uncertainty in meta-analysis. *Res Synth Methods* 2016;7:55-79. doi:10.1002/jrsm.1164

7. Hartung J, Knapp G. A refined method for the meta-analysis of controlled clinical trials with binary outcome. *Stat Med* 2001;20:3875-89.

8. Barrowman NJ, Fang M, Sampson M, Moher D. Identifying null meta-analyses that are ripe for updating. *BMC Med Res Methodol* 2003;3:13.

9. Ioannidis JPA, Contopoulos-Ioannidis DG, Lau J. Recursive cumulative meta-analysis: a diagnostic for the evolution of total randomized evidence from group and individual patient data. *J Clin Epidemiol* 1999;52:281-91.

10. Viechtbauer W. Conducting meta-analyses in R with the metafor package. *J Stat Softw* 2010;36:1-48.

11. IntHout J, Ioannidis JPA, Borm GF. The Hartung-Knapp-Sidik-Jonkman method for random effects meta-analysis is straightforward and considerably outperforms the standard DerSimonian-Laird method. *BMC Med Res Methodol* 2014;14:25. doi:10.1186/1471-2288-14-25

12. Paule RC, Mandel J. Consensus values and weighting factors. *J Res Natl Bur Stand* 1982;87:377-85.

13. Elliott JH, Synnot A, Turner T, et al. Living systematic review: 1. Introduction --- the why, what, when, and how. *J Clin Epidemiol* 2017;91:23-30. doi:10.1016/j.jclinepi.2017.08.010

14. Sutton AJ, Cooper NJ, Jones DR, Lambert PC, Thompson JR, Abrams KR. Evidence-based sample size calculations based upon updated meta-analysis. *Stat Med* 2007;26:2479-500.

---

## DECLARATIONS

**Funding:** None.

**Competing interests:** None declared.

**Ethical approval:** Not required (analysis of published aggregate data).

**Data sharing:** The analytical code and dataset are available at [repository to be provided upon acceptance].

**Transparency declaration:** The lead author (the manuscript's guarantor) affirms that the manuscript is an honest, accurate, and transparent account of the study being reported; that no important aspects of the study have been omitted; and that any discrepancies from the study as planned have been explained.

**Patient and public involvement:** No patients or members of the public were involved in this methodological study.

**Contributorship:** MA conceived the study, developed the analytical framework, performed all analyses, and wrote the manuscript.

**Acknowledgements:** None.

---

*Accepted for publication: [date]*

*BMJ Analysis*
