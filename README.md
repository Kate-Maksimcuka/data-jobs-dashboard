# Data Jobs Dashboard

A beginner-friendly data analysis and visualisation project exploring junior data job postings.

The project analyses a small sample dataset of junior data roles and creates dashboard-style charts showing role types, requested skills, work patterns and salary differences.

## Project Summary

This project is designed to answer practical questions for someone applying to junior data roles:

- Which skills appear most often?
- How common are data analyst, data engineer and data science roles?
- Are junior data jobs more often remote, hybrid or on-site?
- Which role categories have higher average salaries?
- How do requested skills differ by role type?

The dataset is a small synthetic/sample dataset created for portfolio practice. It is not intended to represent the full UK job market.

## Key Skills Demonstrated

- Cleaned and analysed tabular data with pandas
- Split multi-value skills into analyzable rows
- Created summary tables for roles, skills, locations and work types
- Built simple dashboard-style charts
- Compared skills across role categories
- Communicated findings clearly in a README

## Tools Used

- Python
- pandas
- matplotlib
- CSV data
- GitHub

## Project Structure

```text
.
├── data/                     # Sample job postings dataset
├── src/                      # Analysis script
├── outputs/
│   ├── charts/               # Generated dashboard charts
│   └── tables/               # Summary tables
├── docs/                     # Additional notes if needed
├── requirements.txt
└── README.md
```

## Dataset Columns

The dataset contains 30 sample junior data job postings with these fields:

- `job_id`
- `job_title`
- `company`
- `location`
- `work_type`
- `role_category`
- `salary_gbp`
- `skills`
- `posting_date`

## Key Insights

- The dataset contains 30 junior data job postings.
- SQL is the most requested skill in the sample dataset.
- Python appears across data analyst, data engineering, analytics engineering and data science roles.
- Hybrid roles are common in the sample, but remote roles are also well represented.
- Data engineering and analytics engineering roles have higher average salaries than most analyst roles in this sample.
- dbt appears mainly in analytics engineering/data engineering roles, while Power BI and Excel appear mainly in analyst roles.

## Charts

### Most Requested Skills

![Most requested skills](outputs/charts/most_requested_skills.png)

### Role Category Breakdown

![Role category breakdown](outputs/charts/role_category_breakdown.png)

### Remote, Hybrid and On-site Split

![Work type split](outputs/charts/work_type_split.png)

### Average Salary by Role

![Average salary by role](outputs/charts/average_salary_by_role.png)

### Top Skills by Role Category

![Top skills by role category](outputs/charts/top_skills_by_role_category.png)

## Output Tables

The analysis script also creates summary CSV tables:

- `outputs/tables/skill_counts.csv`
- `outputs/tables/role_skill_counts.csv`
- `outputs/tables/role_summary.csv`
- `outputs/tables/work_type_summary.csv`
- `outputs/tables/location_summary.csv`

## How to Run Locally

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install requirements:

```bash
pip install -r requirements.txt
```

Run the analysis:

```bash
MPLCONFIGDIR=.cache/matplotlib XDG_CACHE_HOME=.cache python src/analyse_job_postings.py
```

## What I Practised

- Structuring a small data analysis project
- Cleaning a dataset for analysis
- Working with categorical data and multi-value skill fields
- Creating visual summaries for a dashboard-style README
- Writing clear insights for a non-technical audience

## Next Improvements

- Replace the sample dataset with real job posting data from a saved export
- Add an interactive Streamlit dashboard
- Add filters by location, role type and work pattern
- Track skill demand over time
