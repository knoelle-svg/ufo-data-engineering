import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_PATH = "ufo.db"
DOCS_DIR = "docs"


# -----------------------------
# SQL-driven analyses (meets "pure SQL" requirement)
# -----------------------------
def sightings_by_decade_sql(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Pure SQL: sightings by decade.
    Requires date_time stored as ISO 8601 text (YYYY-MM-DD HH:MM:SS) so strftime works.
    """
    query = """
    SELECT
      (CAST(strftime('%Y', date_time) AS INTEGER) / 10) * 10 AS decade,
      COUNT(*) AS sighting_count
    FROM ufo_sightings
    WHERE date_time IS NOT NULL
      AND strftime('%Y', date_time) IS NOT NULL
    GROUP BY decade
    ORDER BY decade;
    """
    df = pd.read_sql(query, conn)
    print("\nUFO sightings by decade (SQL):")
    print(df)
    return df


def top_countries_post_1955_sql(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Pure SQL: top countries by sightings post-1955.
    """
    query = """
    SELECT
      lower(country) AS country,
      COUNT(*) AS sighting_count
    FROM ufo_sightings
    WHERE date_time IS NOT NULL
      AND strftime('%Y', date_time) IS NOT NULL
      AND CAST(strftime('%Y', date_time) AS INTEGER) >= 1955
      AND country IS NOT NULL
    GROUP BY lower(country)
    ORDER BY sighting_count DESC
    LIMIT 10;
    """
    df = pd.read_sql(query, conn)
    print("\nTop countries by reported UFO sightings post-1955 (SQL):")
    print(df)
    return df


def encounter_duration_summary_sql(conn: sqlite3.Connection) -> pd.DataFrame:
    """
    Pure SQL: basic duration summary.
    """
    query = """
    SELECT
        COUNT(*) AS n_rows,
        AVG(encounter_length) AS avg_seconds,
        MIN(encounter_length) AS min_seconds,
        MAX(encounter_length) AS max_seconds
    FROM ufo_sightings
    WHERE encounter_length IS NOT NULL
      AND encounter_length > 0;
    """
    df = pd.read_sql(query, conn)
