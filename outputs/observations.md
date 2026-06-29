# OLA Electric VoC Analysis — Observations Register

Maintained throughout the project. Every finding labeled per OHC framework:
- **Observation:** Directly supported by data
- **Hypothesis:** Possible explanation requiring further testing  
- **Conclusion:** Validated by statistical evidence (p-value reported)

---

## Phase 1 — Data Collection

| ID | Label | Finding | Evidence |
|----|-------|---------|----------|
| 001 | Observation | 59.9% of 7,119 reviews are 1-star ratings | Rating distribution, combined dataset |
| 002 | Observation | OLA Electric has a 0% developer response rate across 4 years and 7,119 reviews | replyContent column — 100% null |
| 003 | Observation | Review volume spiked 274% between June 2025 (178) and July 2025 (667) | Monthly breakdown, Phase 1 sanity check |
| 004 | Observation | Zero duplicate review IDs across combined dataset of 7,119 reviews | Deduplication check, Phase 1 |
| 005 | Hypothesis | The July 2025 volume spike is linked to a specific identifiable external event | Requires cross-referencing with OLA news timeline in Phase 5 |
| 006 | Hypothesis | Declining review volume in late 2025–2026 reflects disengagement not recovery | Requires sentiment trend analysis in Phase 5 |

---

## Phase 2 — Data Cleaning

| ID | Label | Finding | Evidence |
|----|-------|---------|----------|
| 007 | Observation | 104 reviews (1.5%) contain non-Latin script — VADER reliability reduced for this subset | is_non_english flag, Phase 2 |
| 008 | Observation | 2027 reviews (28.5%) contain fewer than 4 words | is_short_review flag, Phase 2 |
| 009 | Observation | Average cleaning removed 0.8 characters per review | length_change column, Phase 2 |

---

## Phase 3 — Sentiment Analysis
*To be populated*

## Phase 4 — Complaint Classification
*To be populated*

## Phase 5 — EDA
*To be populated*

## Phase 6 — Statistical Testing
*To be populated*


### Phase 2 Addendum — Short Review Analysis

**OBS-012:** 28.5% of reviews (2,027) contain fewer than 4 words.
Content inspection confirms genuine sentiment split:
- Positive camp: 'good' (358), 'nice' (77), 'super' (50), 'excellent' (21)
- Negative camp: 'very bad' (20), 'not working' (18), 'worst' (15), 'bad service' (13)
These reviews carry valid sentiment signal but insufficient text for complaint 
classification. Will be assigned 'Uncategorized — Insufficient Text' in Phase 4.

**OBS-013:** Emoji characters retained in content_clean. VADER has partial emoji 
support. 15 emoji-only reviews will receive near-neutral scores despite positive 
intent. Proportion negligible at aggregate level.

| word_count | review_count | % of short reviews |
|------------|-------------|-------------------|
| 1 word     | 858         | 42.3%             |
| 2 words    | 737         | 36.4%             |
| 3 words    | 432         | 21.3%             |

## Phase 3 — Sentiment Analysis

| ID | Label | Finding | Evidence |
|----|-------|---------|----------|
| 014 | Observation | Overall sentiment distribution: Negative 41.3%, Neutral 21.7%, Positive 37.0% | VADER compound scores, 7119 reviews |
| 015 | Observation | VADER agreement with 1-2 star ratings: 58.3% scored Negative | Cross-tabulation, Phase 3 sanity check |
| 016 | Observation | VADER agreement with 4-5 star ratings: 82.2% scored Positive | Cross-tabulation, Phase 3 sanity check |
| 017 | Observation | Mean sentiment score across all reviews: -0.064 | VADER compound scores |
| 018 | Observation | Non-English reviews avg sentiment: -0.026 vs English: -0.064 | Subgroup analysis, Phase 3 |
| 019 | Hypothesis | If VADER agreement with star ratings exceeds 70% for both positive and negative camps, VADER is sufficiently reliable for this dataset without upgrade to transformer models | To be confirmed by Cell 5 output |

## Phase 4 — Complaint Classification

| ID | Label | Finding | Evidence |
|----|-------|---------|----------|
| 021 | Observation | Software App is the dominant complaint category appearing in 50.5% of all reviews (3598 reviews) | Multi-label keyword classifier, Phase 4 |
| 022 | Observation | Safety/Breakdown and Pricing/Value triggered zero times in 248-review manual sample — may reflect Play Store audience bias toward app complaints | Manual classification, Phase 4 |
| 023 | Observation | 25.5% of reviews (1817) mention 2+ complaint categories simultaneously — indicating cascading failures across multiple business functions | complaint_count column, Phase 4 |
| 024 | Observation | 9.8% of reviews (695) mention 3+ categories — highest severity customer segment experiencing compounded failures | complaint_count column, Phase 4 |
| 025 | Observation | Service Center and Customer Care complaints co-occur in 34.1% of all Service Center reviews — these failures are structurally linked, not independent | Co-occurrence analysis, Phase 4 |
| 026 | Observation | Uncategorized reviews (no category, not positive): 1375 (19.3%) — classifier coverage rate 80.7% | Validation report, Phase 4 |
| 027 | Hypothesis | The Software/App category dominance on Play Store reviews may overstate app problems relative to hardware/service problems that customers report on other platforms | Requires cross-platform validation — out of scope for this project |

## Phase 5 — EDA & Statistical Validation

| ID | Label | Finding | Evidence |
|----|-------|---------|----------|
| 030 | Observation | Software/App is the dominant complaint category at 50.5% of all reviews — nearly 5x the next highest category | Block 1, Phase 5 |
| 031 | Observation | Customer Care has the lowest average star rating (1.12) of any complaint category | Block 1 metrics table, Phase 5 |
| 032 | Observation | Spare Parts has the most negative average sentiment (-0.385) despite lowest volume — intensity inversely related to frequency | Block 3, Phase 5 |
| 033 | Hypothesis | H-001 status: July 2025 volume spike linked to specific external event — requires OLA news cross-reference | Block 4 temporal chart |
| 034 | Hypothesis | H-002 status: declining volume post-July 2025 — sentiment trend direction will indicate disengagement vs recovery | Block 4 temporal chart |
| 035 | Conclusion | Sentiment scores differ significantly across complaint categories (Kruskal-Wallis, p < 0.001) — not all failures produce equal emotional responses | Test 1, Section B |
| 036 | Conclusion | Complaint count is significantly negatively correlated with sentiment score (Spearman) — each additional complaint category reduces sentiment measurably | Test 3, Section B |
