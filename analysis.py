import os
import sqlite3
import pandas as pd

DB_PATH = "ufo.db"
EXPORT_DIR = "exports"


# -----------------------------
# Helpers
# -----------------------------
def connect_db(db_path: str = DB_PATH) -> sqlite3.Connection:
    return sqlite3.connect(db_path)


def ensure_export_dir(path: str = EXPORT_DIR) -> None:
    os.makedirs(path, exist_ok=True)


def parse_ufo_datetime(series: pd.Series) -> pd.Series:
    """
    Parse the dataset's date_time field safely.

    The TidyTuesday UFO dataset documents date_time as mdy h:m.
    In practice, historical data can contain inconsistent formats, so we:
      1) try a common explicit format first
      2) fall back to pandas' parser if needed
    """
    dt = pd.to_datetime(series, format="%m/%d/%y %H:%M", errors="coerce")
    missing = dt.isna()
    if missing.any():
        dt.loc[missing] = pd.to_datetime(series.loc[missing], errors="coerce")
    return dt


def map_region(country: str) -> str:
    """
    Regions are coarse groupings intended to compare reporting patterns,
    not exact geopolitical classifications.
    """
    c = (country or "").lower()
    if c == "us":
        return "United States"
    elif c in {"uk", "gb", "fr", "de", "it", "es", "nl", "se", "no", "fi", "dk", "be", "ch", "ie"}:
        return "Europe"
    elif c in {"jp", "cn", "in", "kr", "sg", "th", "ph", "vn", "my", "id"}:
        return "Asia"
    else:
        return "Other"


# -----------------------------
# Analyses
# -----------------------------
def sightings_by_decade(conn: sqlite3.Connection) -> pd.DataFrame:
    query = """
    SELECT date_time
    FROM ufo_sightings
    WHERE date_time IS NOT NULL;
    """
    df = pd.read_sql(query, conn)
    df["date_time"] = parse_ufo_datetime(df["date_time"])
    df = df.dropna(subset=["date_time"])

    df["decade"] = (df["date_time"].dt.year // 10) * 10
    out = (
        df.groupby("decade")
        .size()
        .reset_index(name="sighting_count")
        .sort_values("decade")
    )

    print("\nUFO sightings by decade:")
    print(out)
    return out


def us_state_concentration(conn: sqlite3.Connection) -> pd.DataFrame:
    query = """
    SELECT state, COUNT(*) AS sighting_count
    FROM ufo_sightings
    WHERE country = 'us' AND state IS NOT NULL
    GROUP BY state
    ORDER BY sighting_count DESC;
    """
    df = pd.read_sql(query, conn)

    total = df["sighting_count"].sum()
    df["cumulative_count"] = df["sighting_count"].cumsum()
    df["cumulative_percent"] = (df["cumulative_count"] / total * 100).round(1)

    print("\nState-level concentration of U.S. UFO sightings (top 10):")
    print(df.head(10))
    return df


def encounter_duration_reporting(conn: sqlite3.Connection) -> dict:
    query_summary = """
    SELECT
        COUNT(*) AS n_rows,
        AVG(encounter_length) AS avg_seconds,
        MIN(encounter_length) AS min_seconds,
        MAX(encounter_length) AS max_seconds
    FROM ufo_sightings
    WHERE encounter_length IS NOT NULL AND encounter_length > 0;
    """
    df_summary = pd.read_sql(query_summary, conn)
    print("\nEncounter length summary (SQL):")
    print(df_summary)

    query_values = """
    SELECT encounter_length
    FROM ufo_sightings
    WHERE encounter_length IS NOT NULL AND encounter_length > 0;
    """
    df = pd.read_sql(query_values, conn)
    df["encounter_length"] = pd.to_numeric(df["encounter_length"], errors="coerce")
    df = df.dropna()

    p50 = df["encounter_length"].quantile(0.50)
    p90 = df["encounter_length"].quantile(0.90)
    p99 = df["encounter_length"].quantile(0.99)

    share_under_60 = (df["encounter_length"] <= 60).mean() * 100
    share_under_300 = (df["encounter_length"] <= 300).mean() * 100
    share_under_1800 = (df["encounter_length"] <= 1800).mean() * 100

    print("\nEncounter length distribution (seconds):")
    print(f"Median (p50): {p50:.0f} sec")
    print(f"90th percentile (p90): {p90:.0f} sec")
    print(f"99th percentile (p99): {p99:.0f} sec")

    print("\nShare of encounters under key thresholds:")
    print(f"<= 60 sec:  {share_under_60:.1f}%")
    print(f"<= 5 min:   {share_under_300:.1f}%")
    print(f"<= 30 min:  {share_under_1800:.1f}%")

    return {"summary_sql": df_summary, "duration_values": df}


def region_by_decade(conn: sqlite3.Connection) -> pd.DataFrame:
    query = """
    SELECT date_time, country
    FROM ufo_sightings
    WHERE date_time IS NOT NULL AND country IS NOT NULL;
    """
    df = pd.read_sql(query, conn)
    df["date_time"] = parse_ufo_datetime(df["date_time"])
    df = df.dropna(subset=["date_time"])

    df["decade"] = (df["date_time"].dt.year // 10) * 10
    df["region"] = df["country"].astype(str).apply(map_region)

    out = (
        df.groupby(["region", "decade"])
        .size()
        .reset_index(name="sighting_count")
        .sort_values(["region", "decade"])
    )

    core = out[out["region"].isin(["United States", "Europe", "Asia"])]

    print("\nCore regional comparison (US vs Europe vs Asia) by decade:")
    print(core)

    return out


def top_countries_post_1955(conn: sqlite3.Connection) -> pd.DataFrame:
    query = """
    SELECT date_time, country
    FROM ufo_sightings
    WHERE date_time IS NOT NULL AND country IS NOT NULL;
    """
    df = pd.read_sql(query, conn)
    df["date_time"] = parse_ufo_datetime(df["date_time"])
    df = df.dropna(subset=["date_time"])

    df = df[df["date_time"].dt.year >= 1955]

    out = (
        df.groupby(df["country"].astype(str).str.lower())
        .size()
        .reset_index(name="sighting_count")
        .sort_values("sighting_count", ascending=False)
    )

    print("\nTop countries by reported UFO sightings (post-1955):")
    print(out.head(10))
    return out


# -----------------------------
# Exports (optional)
# -----------------------------
def export_for_optional_viz(
    decade_counts: pd.DataFrame,
    state_counts: pd.DataFrame,
    duration_values: pd.DataFrame,
    export_dir: str = EXPORT_DIR
) -> None:
    ensure_export_dir(export_dir)

    decade_counts.to_csv(os.path.join(export_dir, "sightings_by_decade.csv"), index=False)
    state_counts.head(10).to_csv(os.path.join(export_dir, "top_states_concentration_top10.csv"), index=False)
    state_counts.to_csv(os.path.join(export_dir, "state_concentration_all_states.csv"), index=False)

    dv = duration_values.copy()
    dv["duration_minutes"] = dv["encounter_length"] / 60

    bins = [0, 1, 5, 30, 60, 240, 10**9]
    labels = ["<=1 min", "1–5 min", "5–30 min", "30–60 min", "1–4 hr", ">4 hr"]

    dv["duration_bin"] = pd.cut(
        dv["duration_minutes"],
        bins=bins,
        labels=labels,
        include_lowest=True
    )

    duration_bins = (
        dv["duration_bin"]
        .value_counts()
        .reindex(labels)
        .fillna(0)
        .astype(int)
        .reset_index()
    )
    duration_bins.columns = ["duration_bin", "count"]
    duration_bins.to_csv(os.path.join(export_dir, "encounter_duration_bins.csv"), index=False)

    print("\nExported CSVs to exports/ folder:")
    print(" - exports/sightings_by_decade.csv")
    print(" - exports/top_states_concentration_top10.csv")
    print(" - exports/state_concentration_all_states.csv")
    print(" - exports/encounter_duration_bins.csv")


# -----------------------------
# Main
# -----------------------------
def main() -> None:
    conn = connect_db(DB_PATH)
    try:
        print("Connected to ufo.db")

        decade_counts = sightings_by_decade(conn)
        state_counts = us_state_concentration(conn)
        duration_results = encounter_duration_reporting(conn)

        # Depth / interest additions
        region_by_decade(conn)
        top_countries_post_1955(conn)

        # Optional exports for later visualization
        export_for_optional_viz(
            decade_counts=decade_counts,
            state_counts=state_counts,
            duration_values=duration_results["duration_values"],
            export_dir=EXPORT_DIR
        )

        print("\nAnalysis complete.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()