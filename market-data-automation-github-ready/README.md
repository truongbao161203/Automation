# Market Data Automation Pipeline

A portfolio-safe demo of a real workflow I built to reduce repetitive market-data collection and cleaning work.

## Problem
A recurring market-research workflow required manually collecting and cleaning pricing and competitor data before updating a shared reporting file.

## Solution
I built a Python-based workflow to:
1. collect structured market data;
2. standardize project, unit, area, and price fields;
3. validate missing or invalid values;
4. calculate price per square meter;
5. remove duplicate records;
6. append clean records to a historical dataset;
7. export a reporting-ready file.

In the original work environment, the collection step used **Python + Playwright** for web data collection. This public repository uses fictional CSV data so no company data, credentials, cookies, private URLs, or proprietary datasets are exposed.

## Outcome
The real workflow reduced a recurring manual data-collection task from approximately **8 hours to around 4 hours**, while keeping a manual validation step before any figures were used in reporting.

## Tech
- Python
- Playwright (original collection workflow)
- CSV / Excel-style structured data
- AI-assisted development
- Data validation and deduplication

## Demo
Install:
```bash
pip install -r requirements.txt
```

Run:
```bash
python main.py
```

The script reads `data/sample_input.csv` and creates:
- `output/sample_output.csv`
- `output/rejected_records.csv`
- `output/history.csv`

## Workflow
```text
Raw data
  ↓
Standardize fields
  ↓
Validate records
  ↓
Calculate price / m²
  ↓
Deduplicate
  ↓
Append history
  ↓
Reporting-ready output
```

## Why manual validation still matters
Automation improves speed and consistency, but it does not remove the need for judgment. Early versions sometimes returned missing or silently incorrect values, so I added step-by-step validation and retained a manual cross-check before data reached a report.

## What I learned
The goal was not coding by itself. The goal was to reduce repetitive work, improve consistency, and create more time for analysis.

## Repository structure
```text
market-data-automation/
├── README.md
├── main.py
├── requirements.txt
├── .gitignore
├── data/
│   └── sample_input.csv
└── output/
    ├── sample_output.csv
    ├── rejected_records.csv
    └── history.csv
```

## Notes
- All data in this repository is fictional.
- The public demo focuses on the transformation and validation pipeline rather than production scraping targets.
