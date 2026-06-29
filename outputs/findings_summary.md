# OLA Electric — Voice of Customer Crisis Analysis
## Findings Summary & Business Recommendations

**Prepared by:** Naren Karthikeyan A  
**Data period:** May 2022 — June 2026  
**Total reviews analyzed:** 7,119  
**Methodology:** Multi-label keyword classification + VADER sentiment analysis  
**Validation:** 99.2% classifier agreement rate on 248 manually labeled reviews

---

## 1. Executive Summary

OLA Electric's customer experience crisis is real, measurable, and sustained.
Analysis of 7,119 Google Play Store reviews spanning four years
reveals an overall average rating of 2.27/5.0, with
59.9% of reviews rated 1-star. The crisis is not driven by a
single failure — it is a systemic breakdown across software, after-sales
service, and customer support, with each failure amplifying the others.
Despite a partial sentiment recovery in 2026, average ratings remain below
3.0 and the brand has not returned to positive sentiment territory at any
point since early 2023.

---

## 2. Key Findings

### Finding 1 — Software is the Most Widespread Failure
**Observation:** Software/App complaints appear in
50.5% of all reviews
(3,598 reviews) — the dominant complaint
category by a significant margin, nearly 5x the next highest category.

**Evidence:** Multi-label keyword classifier, 99.2% validated accuracy.
Average star rating for Software/App complaints: 
1.68/5.0.
72.1% of these reviews are 1-star.

**Implication:** The OLA Electric app is the primary interface between the
customer and their scooter. Every app failure degrades the entire ownership
experience regardless of whether the physical product is functioning correctly.

---

### Finding 2 — Customer Care is the Most Severe Failure
**Observation:** Customer Care complaints produce a 93.9%
one-star rate — the highest of any complaint category — and the lowest average
rating (1.12/5.0).

**Evidence:** Block 7 rating heatmap. Kruskal-Wallis confirms sentiment
differs significantly across categories (H=274.324, p<0.001).

**Implication:** When a customer contacts OLA's support system and receives
no resolution, the relationship is effectively lost. Customer care failure
is the single most consistent predictor of the worst possible customer outcome.

---

### Finding 3 — Service Center and Customer Care Failures Are Structurally Linked
**Observation:** Service Center and Customer Care complaints co-occur in
271 reviews — the 5th highest co-occurrence pair. Service Center carries
88.7% one-star rate and
1.28 average rating.

**Evidence:** Co-occurrence analysis, Block 6. Service center delays generate
customer care contact; customer care non-response amplifies service frustration.
These are not independent failures.

**Implication:** Fixing one without the other produces incomplete relief.
A customer whose scooter is repaired but whose 47 calls went unanswered
will still write a 1-star review.

---

### Finding 4 — App Failure Connects Every Other Complaint
**Observation:** Software/App appears in 6 of the top 10 co-occurring
complaint pairs, including the dominant pair:
Software/App + Battery & Range (558 co-occurrences).

**Evidence:** Co-occurrence heatmap and top 10 pairs table, Block 6.

**Implication:** The app is not just a standalone complaint — it is the
connective tissue through which every other failure is experienced. Battery
status is read through the app. Service is booked through the app. Complaints
are raised through the app. When the app fails, every other system becomes
inaccessible simultaneously.

---

### Finding 5 — A Satisfied Customer Segment Exists and Is Recoverable
**Observation:** 2,078 reviews
(29.2%) contain explicit
positive language. 25 reviews simultaneously flag Software/App complaint
AND Positive Experience — customers who like the scooter but hate the app.

**Evidence:** Block 9 positive experience contrast analysis.

**Implication:** OLA Electric has a core of satisfied customers who value
the physical product. These customers are at risk of churning due to software
and service failures rather than product dissatisfaction. They are the
highest-priority retention segment.

---

### Finding 6 — The Crisis Has a Measurable Arc
**Observation:** Monthly average sentiment declined from +0.38 in mid-2022
to a crisis floor of -0.32 in early 2025, followed by partial recovery
to near-zero in 2026. Review volume peaked at 667 in July 2025 — 274%
above the previous month.

**Evidence:** Block 4 temporal trend analysis. Mann-Whitney U confirms
pre vs post-July 2025 sentiment shift is statistically significant
(p=3.74e-50).

**Implication:** The crisis had a beginning and shows directional improvement.
However, improvement in sentiment scores reflects reviewer population change
(disengagement of most negative customers) rather than genuine service
recovery — average star ratings remain below 3.0 throughout 2026.

---

### Finding 7 — Zero Developer Engagement Across Four Years
**Observation:** OLA Electric has maintained a 0% developer response rate
on Google Play Store across 7,119 reviews spanning four years.

**Evidence:** replyContent column — 100% null across entire dataset.

**Implication:** Industry benchmark for consumer apps is 40-60% response
rate on negative reviews. Zero engagement on a public platform signals
to prospective customers that complaints are ignored. A single visible,
empathetic response to a high-thumbs-up complaint costs minutes and
communicates accountability to thousands of readers.

---

### Finding 8 — Longer Reviews Signal Deeper Damage
**Observation:** Word count is negatively correlated with sentiment score
(Spearman r=-0.369, p<0.001) — the strongest correlation in this project.
Longer reviews are almost always more negative.

**Evidence:** Test 4, Section B statistical validation.

**Implication:** Review length is a reliable early-warning signal for
high-severity complaints. A complaint monitoring system that prioritizes
long, negative reviews for immediate human escalation would surface the
most damaged customer relationships efficiently.

---

## 3. Root Cause Analysis

The data supports a single unified root cause narrative:

> OLA Electric scaled customer acquisition faster than it scaled
> customer experience infrastructure.

The evidence chain:

Aggressive sales growth (2022-2024)

↓

Service center capacity not scaled proportionally

↓

Repair backlogs build → spare parts shortages emerge

↓

Customers unable to get resolutions → flood customer care

↓

Customer care overwhelmed → tickets expire unresolved

↓

App fails to provide visibility or alternative resolution path

↓

Customers escalate to public platforms (Play Store, Twitter)

↓

Rating decline → new buyer hesitation → market share loss

↓

38.83% market share (Jul 2024) → 17.35% (Jul 2025)

Every complaint category in this analysis is a symptom of this
single structural failure. The categories are not independent problems
— they are linked consequences of scaling sales without scaling service.

---

## 4. Business Recommendations

Prioritized by: severity (avg rating + one-star rate) × volume × fixability

---

### Recommendation 1 — Fix the App Immediately (High Volume, High Fixability)
**Priority:** Urgent  
**Category addressed:** Software / App (50.5% of reviews)  
**Function owner:** Product & Engineering  

The app is broken for a significant proportion of users — login failures,
connectivity errors, incorrect data display, and missing features are
documented across thousands of reviews. Unlike service center capacity
(which requires physical infrastructure investment), app fixes are
deployable immediately through OTA updates.

**Specific actions:**
- Prioritize connectivity stability (Bluetooth F002 error appears repeatedly)
- Fix login/authentication failures (blank screen, loading loops)
- Restore accurate battery and location display
- Implement push notifications for charging status
- Add dark mode and ride history (repeatedly requested features)

**Expected impact:** Reducing Software/App complaint rate by 50% would
remove this complaint from ~25% of all reviews — the single largest
improvement available through any intervention.

---

### Recommendation 2 — Rebuild Customer Care as Priority Infrastructure
**Priority:** Critical  
**Category addressed:** Customer Care (10.0% of reviews, 93.9% one-star rate)  
**Function owner:** Customer Experience  

Customer care failure is the most reliable predictor of the worst customer
outcome in this dataset. A 93.9% one-star rate means almost no customer
who contacts support walks away satisfied. This is not a training problem
— it is a structural capacity and process problem.

**Specific actions:**
- Publish and enforce maximum response time SLAs (target: 24 hours)
- Implement ticket tracking visible to customers in the app
- Escalation path: unresolved tickets auto-escalate to senior staff at 48h
- Begin responding to Google Play Store reviews — start with
  high-thumbs-up negative reviews (publicly visible, high reach)
- Report monthly resolution rate as a public metric (accountability signal)

**Expected impact:** Even a 30% improvement in customer care resolution
rate would directly address the category with the highest damage-per-customer
ratio in the dataset.

---

### Recommendation 3 — Treat Service Center + Spare Parts as One System
**Priority:** High  
**Categories addressed:** Service Center (10.4%), Spare Parts (2.0%)  
**Function owner:** Operations + Procurement  

Co-occurrence analysis confirms these failures travel together.
A customer whose scooter sits at a service center for months waiting
for parts experiences both failures simultaneously. Spare Parts has
the most negative average sentiment (-0.385) despite the lowest volume
— when parts are unavailable, the experience is catastrophic.

**Specific actions:**
- Implement minimum spare parts inventory requirements at each service center
- Create a parts availability dashboard visible to service center staff
- Publish estimated repair timelines at job card creation (set expectations)
- Proactive SMS/app notification when parts arrive and repair begins
- Target: maximum 15-day repair turnaround for common components

**Expected impact:** Reducing service center wait times addresses the
category with the second-lowest average rating (1.28) and highest
co-occurrence with customer care escalation.

---

### Recommendation 4 — Activate Play Store as a Customer Recovery Channel
**Priority:** Medium  
**Finding addressed:** 0% developer response rate across 4 years  
**Function owner:** Customer Experience / Marketing  

Zero responses across 7,119 reviews is a missed recovery
opportunity at scale. Each response to a public review is read by
hundreds of prospective customers evaluating OLA Electric.

**Specific actions:**
- Assign dedicated resource for Play Store review responses
- Priority queue: 1-star reviews with 10+ thumbs-up (highest reach)
- Response template: acknowledge + ticket number + resolution timeline
- Target: 40% response rate on 1-star reviews within 30 days
- Track: does responded-to review get updated to higher rating?

**Expected impact:** Measurable improvement in prospective buyer perception.
Visible accountability signals to the market that OLA Electric takes
complaints seriously — partially offsetting negative rating impact.

---

### Recommendation 5 — Implement Early Warning System
**Priority:** Medium-term  
**Finding addressed:** Review length correlates with damage severity  
**Function owner:** Data / Product  

Word count is the strongest predictor of sentiment severity in this
dataset (Spearman r=-0.369). A simple automated system monitoring
review length + sentiment score could surface high-damage complaints
for immediate human escalation before they accumulate thumbs-up votes
and influence prospective buyers.

**Specific actions:**
- Build automated Play Store review monitoring pipeline
- Flag: review length > 100 words AND sentiment score < -0.5
- Auto-create internal ticket for flagged reviews within 2 hours
- Monthly dashboard: complaint category trend with 3-month forecast

---

## 5. KPIs to Track Recovery

If OLA Electric implements these recommendations, the following
metrics — all measurable from public Play Store data — would indicate
genuine recovery:

| KPI | Current | Target | Timeframe |
|-----|---------|--------|-----------|
| Overall avg star rating | 2.27 | 3.5+ | 12 months |
| % 1-star reviews | 59.9% | <35% | 12 months |
| Software/App complaint rate | 50.5% | <25% | 6 months |
| Customer Care 1-star rate | 93.9% | <70% | 9 months |
| Developer response rate | 0% | 40%+ | 3 months |
| Avg sentiment score | -0.064 | >0.10 | 12 months |
| Multi-complaint review rate | 25.5% | <15% | 12 months |

These KPIs can be tracked monthly using the same scraping and
classification pipeline built in this project — making this analysis
a living monitoring tool, not a one-time report.

---

## 6. Methodological Notes

| Decision | Rationale |
|----------|-----------|
| VADER over BERT | Lexicon-based, explainable, validated at 82.2% positive agreement. Upgrade not warranted by evidence. |
| Rule-based over LDA | Quantifying known problems not discovering unknown ones. 99.2% manual validation agreement. |
| Multi-label classification | Real complaints span multiple categories. Single-label would discard signal. |
| Play Store as primary source | Public, free, no authentication, 4-year temporal coverage, Python-native scraping. |
| Star rating as primary health metric | More reliable than VADER for absolute negative sentiment due to factual complaint language patterns in Indian English. |

---

*Analysis conducted using Python (pandas, VADER, scipy, matplotlib, seaborn).  
Full code and data available at: github.com/coderfox-cap*
