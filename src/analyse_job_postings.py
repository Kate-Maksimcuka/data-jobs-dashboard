from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

DATA_PATH = Path("data/job_postings.csv")
OUTPUT_DIR = Path("outputs")
CHART_DIR = OUTPUT_DIR / "charts"
TABLE_DIR = OUTPUT_DIR / "tables"


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, parse_dates=["posting_date"])
    df["salary_gbp"] = pd.to_numeric(df["salary_gbp"])
    df["skills_list"] = df["skills"].str.split(";")
    return df


def build_skill_counts(df: pd.DataFrame) -> pd.DataFrame:
    skills = df[["job_id", "role_category", "skills_list"]].explode("skills_list")
    skills["skill"] = skills["skills_list"].str.strip()
    return (
        skills.groupby("skill")
        .agg(job_count=("job_id", "nunique"))
        .sort_values("job_count", ascending=False)
        .reset_index()
    )


def build_role_skill_counts(df: pd.DataFrame) -> pd.DataFrame:
    skills = df[["job_id", "role_category", "skills_list"]].explode("skills_list")
    skills["skill"] = skills["skills_list"].str.strip()
    return (
        skills.groupby(["role_category", "skill"])
        .agg(job_count=("job_id", "nunique"))
        .reset_index()
        .sort_values(["role_category", "job_count"], ascending=[True, False])
    )


def export_tables(df: pd.DataFrame, skill_counts: pd.DataFrame, role_skill_counts: pd.DataFrame) -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    role_summary = (
        df.groupby("role_category")
        .agg(
            job_count=("job_id", "count"),
            average_salary_gbp=("salary_gbp", "mean"),
            minimum_salary_gbp=("salary_gbp", "min"),
            maximum_salary_gbp=("salary_gbp", "max"),
        )
        .round(0)
        .reset_index()
    )
    work_type_summary = df["work_type"].value_counts().rename_axis("work_type").reset_index(name="job_count")
    location_summary = df["location"].value_counts().rename_axis("location").reset_index(name="job_count")

    role_summary.to_csv(TABLE_DIR / "role_summary.csv", index=False)
    work_type_summary.to_csv(TABLE_DIR / "work_type_summary.csv", index=False)
    location_summary.to_csv(TABLE_DIR / "location_summary.csv", index=False)
    skill_counts.to_csv(TABLE_DIR / "skill_counts.csv", index=False)
    role_skill_counts.to_csv(TABLE_DIR / "role_skill_counts.csv", index=False)


def save_most_requested_skills_chart(skill_counts: pd.DataFrame) -> None:
    top_skills = skill_counts.sort_values("job_count", ascending=True).tail(10)
    plt.figure(figsize=(10, 6))
    plt.barh(top_skills["skill"], top_skills["job_count"])
    plt.title("Most Requested Skills in Junior Data Roles")
    plt.xlabel("Number of job postings")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "most_requested_skills.png", dpi=160)
    plt.close()


def save_role_breakdown_chart(df: pd.DataFrame) -> None:
    role_counts = df["role_category"].value_counts().sort_values(ascending=True)
    plt.figure(figsize=(9, 5))
    plt.barh(role_counts.index, role_counts.values)
    plt.title("Job Postings by Role Category")
    plt.xlabel("Number of job postings")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "role_category_breakdown.png", dpi=160)
    plt.close()


def save_work_type_chart(df: pd.DataFrame) -> None:
    work_counts = df["work_type"].value_counts()
    plt.figure(figsize=(7, 7))
    plt.pie(work_counts.values, labels=work_counts.index, autopct="%1.0f%%", startangle=90)
    plt.title("Remote, Hybrid and On-site Job Split")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "work_type_split.png", dpi=160)
    plt.close()


def save_average_salary_chart(df: pd.DataFrame) -> None:
    salary = df.groupby("role_category")["salary_gbp"].mean().sort_values(ascending=True)
    plt.figure(figsize=(9, 5))
    plt.barh(salary.index, salary.values)
    plt.title("Average Salary by Role Category")
    plt.xlabel("Average salary (£)")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "average_salary_by_role.png", dpi=160)
    plt.close()


def save_role_skill_heatmap(role_skill_counts: pd.DataFrame) -> None:
    top_skills = role_skill_counts.groupby("skill")["job_count"].sum().sort_values(ascending=False).head(8).index
    heatmap_df = role_skill_counts[role_skill_counts["skill"].isin(top_skills)]
    pivot = heatmap_df.pivot_table(
        index="role_category",
        columns="skill",
        values="job_count",
        fill_value=0,
    )

    plt.figure(figsize=(11, 5))
    plt.imshow(pivot.values, aspect="auto")
    plt.title("Top Skills by Role Category")
    plt.xticks(range(len(pivot.columns)), pivot.columns, rotation=45, ha="right")
    plt.yticks(range(len(pivot.index)), pivot.index)
    plt.colorbar(label="Number of postings")

    for row_idx in range(pivot.shape[0]):
        for col_idx in range(pivot.shape[1]):
            plt.text(col_idx, row_idx, int(pivot.iloc[row_idx, col_idx]), ha="center", va="center")

    plt.tight_layout()
    plt.savefig(CHART_DIR / "top_skills_by_role_category.png", dpi=160)
    plt.close()


def write_insights(df: pd.DataFrame, skill_counts: pd.DataFrame) -> None:
    top_skill = skill_counts.iloc[0]
    top_role = df["role_category"].value_counts().idxmax()
    top_work_type = df["work_type"].value_counts().idxmax()
    average_salary = round(df["salary_gbp"].mean())
    median_salary = round(df["salary_gbp"].median())
    minimum_salary = round(df["salary_gbp"].min())
    maximum_salary = round(df["salary_gbp"].max())

    insights = f"""# Key Insights

- The dataset contains {len(df)} junior data job postings.
- The most common role category is **{top_role}**.
- The most requested skill is **{top_skill['skill']}**, appearing in {int(top_skill['job_count'])} postings.
- The most common working pattern is **{top_work_type}**.
- The average listed salary is approximately **£{average_salary:,}**.
- SQL and Python appear frequently across several role types, making them useful core skills for junior data roles.
"""
    (OUTPUT_DIR / "key_insights.md").write_text(insights)

    statistics = f"""# Descriptive Statistics Summary

This summary uses simple descriptive statistics because the dataset is small and synthetic.

## Salary Summary

- Average salary: £{average_salary:,}
- Median salary: £{median_salary:,}
- Minimum salary: £{minimum_salary:,}
- Maximum salary: £{maximum_salary:,}

## Dataset Size

- Total postings: {len(df)}
- Role categories: {df['role_category'].nunique()}
- Locations: {df['location'].nunique()}
- Work types: {df['work_type'].nunique()}
- Unique skills: {skill_counts['skill'].nunique()}
"""
    (OUTPUT_DIR / "descriptive_statistics.md").write_text(statistics)


def main() -> None:
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    df = load_data()
    skill_counts = build_skill_counts(df)
    role_skill_counts = build_role_skill_counts(df)

    export_tables(df, skill_counts, role_skill_counts)
    save_most_requested_skills_chart(skill_counts)
    save_role_breakdown_chart(df)
    save_work_type_chart(df)
    save_average_salary_chart(df)
    save_role_skill_heatmap(role_skill_counts)
    write_insights(df, skill_counts)
    print(f"Saved charts to {CHART_DIR}")
    print(f"Saved tables to {TABLE_DIR}")


if __name__ == "__main__":
    main()
