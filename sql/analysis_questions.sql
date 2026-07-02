-- =====================================================================
-- NHS A&E Performance Analysis: business questions in SQL
-- Answers the five questions in BUSINESS_PROBLEM.md Section 2.
-- Source table: ae_clean (loaded from data/clean/ae_monthly_clean.csv)
-- Engine: DuckDB (ANSI SQL, portable to PostgreSQL and SQL Server)
-- All queries use the trend population only (in_trend_population = TRUE)
-- =====================================================================

-- Q1 ------------------------------------------------------------------
-- National Type 1 four-hour performance by month, and the January dip.
-- Technique: aggregate then window function to compare each month
-- against the previous one.
WITH monthly AS (
    SELECT
        month,
        SUM(type1_attendances)                          AS attendances,
        SUM(type1_over_4hrs)                            AS over_4hrs,
        SUM(dta_12hr_waits)                             AS dta_12hr_waits,
        ROUND(100.0 * (SUM(type1_attendances) - SUM(type1_over_4hrs))
              / SUM(type1_attendances), 1)              AS perf_pct
    FROM ae_clean
    WHERE in_trend_population
    GROUP BY month
)
SELECT
    month,
    attendances,
    perf_pct,
    ROUND(perf_pct - LAG(perf_pct) OVER (ORDER BY month), 1)
        AS perf_change_vs_prev_month,
    dta_12hr_waits
FROM monthly
ORDER BY month;

-- Q2 ------------------------------------------------------------------
-- Which trusts deteriorated most into January, and which recovered
-- fastest by March?
-- Technique: conditional aggregation pivots the three anchor months
-- into columns; minimum volume filter avoids small-denominator noise.
WITH pivoted AS (
    SELECT
        "Org Code"                                       AS org_code,
        MAX("Org name")                                  AS org_name,
        MAX("Parent Org")                                AS region,
        MAX(CASE WHEN month = DATE '2025-10-01' THEN type1_perf_pct END) AS perf_oct,
        MAX(CASE WHEN month = DATE '2026-01-01' THEN type1_perf_pct END) AS perf_jan,
        MAX(CASE WHEN month = DATE '2026-03-01' THEN type1_perf_pct END) AS perf_mar,
        MAX(CASE WHEN month = DATE '2026-01-01' THEN type1_attendances END) AS att_jan
    FROM ae_clean
    WHERE in_trend_population
    GROUP BY "Org Code"
)
SELECT
    org_name,
    region,
    perf_oct,
    perf_jan,
    perf_mar,
    ROUND(perf_jan - perf_oct, 1) AS winter_deterioration,
    ROUND(perf_mar - perf_jan, 1) AS recovery
FROM pivoted
WHERE att_jan >= 3000          -- exclude very small units
ORDER BY winter_deterioration ASC
LIMIT 10;

-- Q3 ------------------------------------------------------------------
-- Regional comparison: is winter deterioration uniform or concentrated?
WITH regional AS (
    SELECT
        "Parent Org"                                     AS region,
        month,
        ROUND(100.0 * (SUM(type1_attendances) - SUM(type1_over_4hrs))
              / SUM(type1_attendances), 1)               AS perf_pct
    FROM ae_clean
    WHERE in_trend_population
    GROUP BY "Parent Org", month
)
SELECT
    region,
    MAX(CASE WHEN month = DATE '2025-10-01' THEN perf_pct END) AS perf_oct,
    MAX(CASE WHEN month = DATE '2026-01-01' THEN perf_pct END) AS perf_jan,
    MAX(CASE WHEN month = DATE '2026-03-01' THEN perf_pct END) AS perf_mar,
    ROUND(MAX(CASE WHEN month = DATE '2026-01-01' THEN perf_pct END)
        - MAX(CASE WHEN month = DATE '2025-10-01' THEN perf_pct END), 1)
        AS winter_deterioration
FROM regional
GROUP BY region
ORDER BY winter_deterioration ASC;

-- Q4 ------------------------------------------------------------------
-- Where are January 12-hour DTA waits concentrated?
-- Technique: window functions build a cumulative share, showing how
-- few trusts account for how much of the national problem.
WITH jan AS (
    SELECT
        "Org name"                                       AS org_name,
        "Parent Org"                                     AS region,
        dta_12hr_waits
    FROM ae_clean
    WHERE in_trend_population
      AND month = DATE '2026-01-01'
      AND dta_12hr_waits > 0
)
SELECT
    org_name,
    region,
    dta_12hr_waits,
    ROUND(100.0 * dta_12hr_waits / SUM(dta_12hr_waits) OVER (), 1)
        AS pct_of_national,
    ROUND(100.0 * SUM(dta_12hr_waits) OVER (
            ORDER BY dta_12hr_waits DESC
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
          / SUM(dta_12hr_waits) OVER (), 1)
        AS cumulative_pct
FROM jan
ORDER BY dta_12hr_waits DESC
LIMIT 15;

-- Q5 ------------------------------------------------------------------
-- Is January deterioration explained by attendance volume?
-- Technique: compare each trust's January attendances against its own
-- Oct-Dec baseline, alongside its performance change, then correlate.
WITH baseline AS (
    SELECT
        "Org Code"                                       AS org_code,
        AVG(CASE WHEN month < DATE '2026-01-01'
                 THEN type1_attendances END)             AS avg_att_oct_dec,
        MAX(CASE WHEN month = DATE '2026-01-01'
                 THEN type1_attendances END)             AS att_jan,
        AVG(CASE WHEN month < DATE '2026-01-01'
                 THEN type1_perf_pct END)                AS avg_perf_oct_dec,
        MAX(CASE WHEN month = DATE '2026-01-01'
                 THEN type1_perf_pct END)                AS perf_jan
    FROM ae_clean
    WHERE in_trend_population
    GROUP BY "Org Code"
)
SELECT
    COUNT(*)                                              AS trusts,
    ROUND(AVG(100.0 * (att_jan - avg_att_oct_dec) / avg_att_oct_dec), 1)
        AS avg_attendance_change_pct,
    ROUND(AVG(perf_jan - avg_perf_oct_dec), 1)
        AS avg_perf_change_pts,
    ROUND(CORR(100.0 * (att_jan - avg_att_oct_dec) / avg_att_oct_dec,
               perf_jan - avg_perf_oct_dec), 3)
        AS corr_volume_change_vs_perf_change
FROM baseline
WHERE avg_att_oct_dec >= 3000;
