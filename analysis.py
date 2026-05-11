import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_PATH = "ufo.db"
EXPORT_DIR = "exports"
DOCS_DIR = "docs"


# -----------------------------
# Helpers
# -----------------------------
def connect_db(db_path: str = DB_PATH) -> sqlite3.Connection:
    return sqlite3.connect(db_path)


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def parse_ufo_datetime(series: pd.Series) -> pd.Series:
    """
    Parse the dataset's date_time field safely.

    The TidyTuesday UFO dataset documents date_time as mdy h:m.
    Historical data can contain inconsistent formats, so we:
      1) try an explicit format
      2) fall back to pandas' parser
    """
    dt = pd.to_datetime(series, format="%m/%d/%y %H:%M", errors="coerce")
    missing = dt.isna()
    if missing.any():
        dt.loc[missing] = pd.to_datetime(series.loc[missing], errors="coerce")
    return dt


def map_region(country: str) -> str:
    """
    Coarse regional grouping intended to compare reporting patterns,
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
# Analysis Queries
# -----------------------------
def sightings_by_decade(conn: sqlite3.Connection) -> pd.DataFrame:
    df = pd.read_sql(
        "SELECT date_time FROM ufo_sightings WHERE date_time IS NOT NULL;",
        conn
    )
    df["date_time"] = parse_ufo_datetime(df["date_time"])
    df = df.dropna(subset=["date_time"])

    df["decade"] = (df["date_time"].dt.year // 10) * 10
    out = df.groupby("decade").size().reset_index(name="sighting_count").sort_values("decade")

    print("\nUFO sightings by decade:")
    print(out)
    return out


def us_state_concentration(conn: sqlite3.Connection) -> pd.DataFrame:
    df = pd.read_sql(
        """
        SELECT state, COUNT(*) AS sighting_count
        FROM ufo_sightings
        WHERE country = 'us' AND state IS NOT NULL
        GROUP BY state
        ORDER BY sighting_count DESC;
        """,
        conn,
    )

    total = df["sighting_count"].sum()
    df["cumulative_percent"] = (df["sighting_count"].cumsum() / total * 100).round(1)

    print("\nTop U.S. states by sightings:")
    print(df.head(10))
    return df


def encounter_duration_reporting(conn: sqlite3.Connection) -> pd.DataFrame:
    df = pd.read_sql(
        """
        SELECT encounter_length
        FROM ufo_sightings
        WHERE encounter_length IS NOT NULL AND encounter_length > 0;
        """,
        conn,
    )

    df["encounter_length"] = pd.to_numeric(df["encounter_length"], errors="coerce")
    df = df.dropna()

    print("\nEncounter duration percentiles (seconds):")
    print(df["encounter_length"].quantile([0.5, 0.9, 0.99]))

    return df


# -----------------------------
# Plots (for Power BI / review)
# -----------------------------
def save_plots(
    decade_counts: pd.DataFrame,
    state_counts: pd.DataFrame,
    duration_values: pd.DataFrame,
    out_dir: str = DOCS_DIR,
) -> None:
    ensure_dir(out_dir)

    # Plot 1: Sightings by decade
    plt.figure()
    plt.plot(decade_counts["decade"], decade_counts["sighting_count"], marker="o")
    plt.title("UFO Sightings by Decade")
    plt.xlabel("Decade")
    plt.ylabel("Reported Sightings")
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "plot_sightings_by_decade.png"))
    plt.close()

    # Plot 2: Top U.S. states (Pareto-style)
    top10 = state_counts.head(10)
    fig, ax1 = plt.subplots()
    ax1.bar(top10["state"], top10["sighting_count"])
    ax1.set_ylabel("Sightings")
    ax1.set_xlabel("State")

    ax2 = ax1.twinx()
    ax2.plot(top10["state"], top10["cumulative_percent"], marker="o", color="orange")
    ax2.set_ylabel("Cumulative %")

    fig.suptitle("Top 10 U.S. States by UFO Sightings")
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "plot_top_states_pareto.png"))
    plt.close(fig)

    # Plot 3: Encounter duration bins
    dv = duration_values.copy()
    dv["minutes"] = dv["encounter_length"] / 60

    bins = [0, 1, 5, 30, 60, 240, 10**9]
    labels = ["≤1 min", "1–5 min", "5–30 min", "30–60 min", "1–4 hr", ">4 hr"]
    dv["bin"] = pd.cut(dv["minutes"], bins=bins, labels=labels, include_lowest=True)

    counts = dv["bin"].value_counts().reindex(labels).fillna(0)

    plt.figure()
    plt.bar(counts.index.astype(str), counts.values)
    plt.title("Reported Encounter Duration Distribution")
    plt.ylabel("Count")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, "plot_encounter_duration_bins.png"))
    plt.close()


# -----------------------------
# Main
# -----------------------------
def main() -> None:
    conn = connect_db()
    try:
        decade_counts = sightings_by_decade(conn)
        state_counts = us_state_concentration(conn)
        duration_values = encounter_duration_reporting(conn)

        save_plots(decade_counts, state_counts, duration_values)

        print("\n✅ Analysis complete. Tables printed; plots saved to docs/.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()