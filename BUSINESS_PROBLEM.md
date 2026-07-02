# Business Problem Document

## NHS A&E Performance Analysis: Winter Pressure and Trust-Level Recovery

**Author:** Auwal Musa
**Date:** July 2026
**Status:** Draft v1.0

---

## 1. Problem Statement

NHS England publishes monthly A&E performance data for around 200 provider organisations, but the raw files answer no management questions on their own. Performance must be derived, department types must be separated, and single-month snapshots hide the trends that matter.

This analysis answers the question a regional operations director would ask each spring:

> **Which trusts deteriorated most under winter pressure, which recovered fastest, and where should improvement support be targeted before next winter?**

## 2. Questions the Analysis Must Answer

1. How did national Type 1 four-hour performance move across the winter period (October 2025 to March 2026), and how severe was the January dip?
2. Which individual trusts deteriorated the most between autumn and January, and which recovered fastest by March?
3. How do the seven NHS England regions compare, and is winter deterioration uniform or concentrated?
4. Where are 12-hour decision-to-admit waits concentrated, and do they track the four-hour measure or tell a different story?
5. Is deterioration explained by attendance volume, or does performance worsen independently of demand?

## 3. Data Source

- **Publisher:** NHS England, Monthly A&E Attendances and Emergency Admissions (official statistics)
- **Files:** Monthly provider-level CSVs, October 2025 to March 2026 (six months)
- **Grain:** one row = one provider organisation, one calendar month
- **Hierarchy:** NHS England Region (Parent Org) > Provider organisation (Org Code, Org Name)
- **Licence:** Open Government Licence; data is public and safe for a published dashboard

## 4. Metric Definitions

| Metric | Definition |
| --- | --- |
| Four-hour performance (Type 1) | (Type 1 attendances minus Type 1 attendances over 4hrs) / Type 1 attendances. Not present in the source data; derived in this analysis. |
| 12-hour DTA waits | Patients waiting 12+ hours from decision to admit to admission, as published. |
| Winter deterioration | Trust-level change in Type 1 four-hour performance, October 2025 baseline vs January 2026. |
| Recovery | Trust-level change in Type 1 four-hour performance, January 2026 vs March 2026. |

## 5. Scope, Exclusions and Data Quality Rules

1. **Exclude aggregate rows.** Source files contain pre-computed England totals which double-count if loaded. Rule: exclude any row where Parent Org = "TOTAL" **or** Period = "TOTAL" (both variants occur). Validated: exactly one aggregate row per file.
2. **Type 1 departments are the headline.** Type 1 (major, consultant-led A&E) is the standard basis for serious performance analysis; Type 2 and Other (walk-in centres, UTCs) handle minor cases and inflate apparent performance. All-types view retained as a secondary toggle.
3. **Analysis population:** the 121 organisations reporting Type 1 activity in every month of the period, ensuring like-for-like trend comparisons.
4. **Case-mix caveat:** children's hospitals consistently outperform general acute trusts; league-table views must be read with case mix in mind and the report will say so.
5. **Period covered:** six months. Findings describe the 2025-26 winter, not long-run structural trends.

## 6. Deliverables

1. Cleaned, combined dataset (Python: ingestion, validation, exclusion rules, derived metrics)
2. SQL analysis answering the five questions above
3. Interactive Power BI dashboard: national trend page and trust drill-down page, published via Publish to web
4. Written findings report leading with recommendations
5. Stakeholder presentation summarising the analysis on one slide per question

## 7. Success Criteria

A reader with no NHS background can open the dashboard and, within one minute, name the worst winter month, the most deteriorated trusts, and the regions where 12-hour waits concentrate. All figures reproducible from raw files by running the published code.
