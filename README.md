# NHS A&E Performance Analysis

Which NHS trusts deteriorated most under winter pressure, which recovered fastest, and where should improvement support be targeted before next winter?

An end-to-end analysis of NHS England Monthly A&E Attendances and Emergency Admissions data (October 2025 to March 2026), built as a Reproducible Analytical Pipeline (RAP).

**Headline finding:** national Type 1 four-hour performance bottomed at 57.0% in January 2026 while 12-hour decision-to-admit waits spiked 41% above surrounding months, despite no unusual attendance volume, indicating a capacity problem rather than a demand problem. By March the system recovered to 63.9%, its best position of the period.

## RAP principles applied

- Open code and open data, version controlled
- Modular pipeline: one module per stage, one function per documented rule
- No manual steps: `python run_pipeline.py` reproduces every output
- Input validation that fails loudly on schema changes
- Unit tests for every cleaning and derivation rule (`pytest`)
- Pinned dependencies (`requirements.txt`)
- A validation report generated on every run for reviewer checking

## Project structure

```
nhs-ae-performance-analysis/
|-- BUSINESS_PROBLEM.md      problem statement, definitions, data quality rules
|-- run_pipeline.py          single entry point
|-- requirements.txt         pinned dependencies
|-- src/
|   |-- config.py            all paths and constants
|   |-- ingest.py            read and validate raw NHS CSVs
|   |-- clean.py             Rule 1: aggregate row exclusion; period parsing
|   |-- derive.py            Rule 2: derived performance; Rule 3: trend population
|   |-- validate.py          validation report
|-- tests/
|   |-- test_pipeline.py     unit tests, one class per rule
|-- data/
|   |-- raw/                 source CSVs as published by NHS England
|   |-- clean/               pipeline outputs
|-- sql/                     business questions answered in SQL (in progress)
|-- dashboard/               Power BI report (in progress)
|-- reports/                 written findings (in progress)
```

## Reproducing the analysis

```
pip install -r requirements.txt
pytest                  # 8 tests covering every documented rule
python run_pipeline.py  # rebuilds data/clean/ from data/raw/
```

## Data source

NHS England, [A&E Attendances and Emergency Admissions](https://www.england.nhs.uk/statistics/statistical-work-areas/ae-waiting-times-and-activity/), monthly provider-level CSVs, published under the Open Government Licence.

Key definitions, exclusions, and known data traps (including the double-counting aggregate rows present in the source files) are documented in [BUSINESS_PROBLEM.md](BUSINESS_PROBLEM.md).

## Author

Auwal Musa | [Portfolio](https://auwalmusa.github.io) | [LinkedIn](https://www.linkedin.com/in/auwal-musa/)
