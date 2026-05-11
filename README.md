# UFO Sightings Data Engineering Exercise

## Overview
This project demonstrates a simple, reproducible data engineering workflow:
- Downloading a public dataset from the web
- Designing and applying a relational schema
- Ingesting data into SQLite
- Answering analytical questions using SQL and Python

The goal is to emphasize clarity, reproducibility, and intentional design decisions over over-engineering.

---


## Data Source

The dataset used in this project is the **TidyTuesday UFO Sightings dataset (2019‑06‑25)**, which contains over 80,000 reported UFO sightings worldwide.

- **Source repository:** https://github.com/rfordatascience/tidytuesday/tree/main/data/2019/2019-06-25 [1](https://github.com/rfordatascience/tidytuesday/tree/main/data/2019/2019-06-25)
- **Raw CSV download:** https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2019/2019-06-25/ufo_sightings.csv [2](https://github.com/rfordatascience/tidytuesday/blob/main/data/2019/2019-06-25/ufo_sightings.csv)
- **Approximate raw size:** ~14 MB uncompressed [2](https://github.com/rfordatascience/tidytuesday/blob/main/data/2019/2019-06-25/ufo_sightings.csv)

This dataset was selected because it is publicly accessible without authentication, large enough to support meaningful analytical exploration, and well‑suited for demonstrating relational modeling and analytical querying over semi‑structured real‑world reports.
```

---

## Schema Design
The database schema is defined explicitly in `schema.sql` rather than relying on automatic type inference. A surrogate primary key is introduced because the source data does not include a unique record identifier.

SQLite data types are chosen for compatibility and analytical simplicity:
- Text fields (e.g., city, shape) use `TEXT`
- Duration values use `REAL`
- Date values are stored as `TEXT` to preserve ISO formatting

Indexes are added to columns commonly used in analytical queries (`state`, `country`, `shape`, `date_time`) to improve query performance.

---

## Ingestion Pipeline
The ingestion process is implemented in `ingest.py` and is fully reproducible. On each run, the script:
1. Downloads the raw CSV dataset
2. Applies the schema defined in `schema.sql`
3. Loads all data into a local SQLite database (`ufo.db`)

Although chunked ingestion is common for large datasets, the UFO dataset is small enough (<100k rows) to be safely processed in memory. For simplicity and readability, the full dataset is ingested in a single pass.

The generated database file is excluded from version control and can be regenerated at any time.

---

## Analysis Approach
Analysis is performed in `analysis.py` using a combination of pure SQL queries and Python-based inspection.

While ingestion and schema design preserve all global records, the analytical questions primarily focus on U.S. sightings. This scoping decision reflects higher data completeness and the availability of standardized state identifiers.

The analysis emphasizes patterns in **human reporting behavior** rather than interpretation of underlying events.

---

## Analysis

### Sightings by Decade
To examine long-term reporting patterns, sightings were grouped by decade based on their reported date. This analysis shows a clear increase in reported sightings beginning in the late 20th century, with particularly strong growth after the 1990s.

Rather than implying changes in underlying phenomena, this trend likely reflects changes in population size, media exposure, internet access, and the ease of reporting over time.

---

### Geographic Concentration of Sightings
To understand whether reports are broadly distributed or geographically concentrated, U.S. sightings were ranked by state and examined cumulatively.

Together, the top five U.S. states account for approximately 35–40% of reported sightings, indicating that reports are moderately concentrated rather than evenly distributed across the country. This suggests geographic clustering and/or differences in reporting behavior.

---

### Encounter Duration and Reporting Behavior
Reported encounter durations are highly right-skewed: most sightings are brief, while a small number of extremely long reports inflate average values. In this dataset, the median reported encounter lasts approximately three minutes, while the 99th percentile extends to several hours.

To make these patterns interpretable, the analysis examines the share of encounters under practical duration thresholds. Approximately 36.7% of reported sightings last one minute or less, 66.5% last five minutes or less, and 91.0% last under 30 minutes.

These results suggest that the dataset primarily reflects brief observational events with a long tail of outliers, consistent with human perception and recall effects rather than uniformly long encounters.

---

## Limitations & Bias
To reduce early-era sparsity and examine modern reporting patterns, sightings were aggregated by country for the post-1955 period. Results show that reported sightings are heavily concentrated in a small number of primarily English-speaking countries, with the United States accounting for the majority of submissions. This concentration likely reflects reporting infrastructure, language accessibility, and the U.S.-centric origins of civilian reporting systems rather than geographic prevalence of events.

---

## Future Work
Future work could incorporate international or government-sourced reporting datasets to evaluate whether observed trends persist across alternative data collection systems.

---

## Entity–Relationship Diagram
docs/er_diagram_ufo_sightings.png


---

## How to Run
Run all commands from the project root.

```bash
pip install -r requirements.txt
python ingest.py
python analysis.py 
```
