from pathlib import Path
import pandas as pd

INPUT_FILE = Path("data/sample_input.csv")
OUTPUT_DIR = Path("output")
CLEAN_FILE = OUTPUT_DIR / "sample_output.csv"
REJECTED_FILE = OUTPUT_DIR / "rejected_records.csv"
HISTORY_FILE = OUTPUT_DIR / "history.csv"

def standardize_text(value):
    if pd.isna(value):
        return ""
    return " ".join(str(value).strip().split())

def clean_and_validate(df):
    data = df.copy()

    for col in ["project", "unit_type", "source"]:
        data[col] = data[col].apply(standardize_text)

    data["area_sqm"] = pd.to_numeric(data["area_sqm"], errors="coerce")
    data["asking_price_vnd"] = pd.to_numeric(data["asking_price_vnd"], errors="coerce")
    data["validation_error"] = ""

    def add_error(mask, message):
        for idx in data.index[mask]:
            current = data.at[idx, "validation_error"]
            data.at[idx, "validation_error"] = f"{current}; {message}".strip("; ")

    add_error(data["project"].eq(""), "missing project")
    add_error(data["unit_type"].eq(""), "missing unit type")
    add_error(data["area_sqm"].isna(), "invalid area")
    add_error(data["asking_price_vnd"].isna(), "invalid asking price")
    add_error(data["area_sqm"].fillna(0) <= 0, "area must be > 0")
    add_error(data["asking_price_vnd"].fillna(0) <= 0, "asking price must be > 0")

    clean = data[data["validation_error"].eq("")].copy()
    rejected = data[~data["validation_error"].eq("")].copy()

    clean["price_per_sqm_vnd"] = (
        clean["asking_price_vnd"] / clean["area_sqm"]
    ).round(0)

    clean = clean.drop_duplicates(
        subset=["project", "unit_type", "area_sqm", "asking_price_vnd", "source"],
        keep="first",
    )
    return clean, rejected

def append_history(clean_df, history_path):
    if history_path.exists():
        history = pd.read_csv(history_path)
        combined = pd.concat([history, clean_df], ignore_index=True)
    else:
        combined = clean_df.copy()

    return combined.drop_duplicates(
        subset=["date", "project", "unit_type", "area_sqm", "asking_price_vnd", "source"],
        keep="last",
    ).sort_values(["date", "project", "unit_type"], ignore_index=True)

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    raw = pd.read_csv(INPUT_FILE)
    clean, rejected = clean_and_validate(raw)

    clean.to_csv(CLEAN_FILE, index=False)
    rejected.to_csv(REJECTED_FILE, index=False)

    history = append_history(clean, HISTORY_FILE)
    history.to_csv(HISTORY_FILE, index=False)

    print(f"Raw records: {len(raw)}")
    print(f"Clean records: {len(clean)}")
    print(f"Rejected records: {len(rejected)}")

if __name__ == "__main__":
    main()
