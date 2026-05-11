# UFO Sightings Data Engineering Exercise

## Overview
This project demonstrates a simple, reproducible data engineering workflow using a public, real‑world dataset. The focus is on clarity, correctness, and reviewer usability rather than over‑engineering.

The pipeline includes:
- Programmatic download of a public dataset
- Relational modeling and ingestion into SQLite
- Analytical querying using SQL and Python
- Generation of tables and lightweight visual artifacts suitable for downstream BI tools (e.g., Power BI)

Execution is fully reproducible and designed to run end‑to‑end with a single command.

---

## Data Source

The dataset used in this project is the **TidyTuesday UFO Sightings dataset (2019‑06‑25)**, which contains over 80,000 reported UFO sightings worldwide.

- **Source repository:** https://github.com/rfordatascience/tidytuesday/tree/main/data/2019/2019-06-25  
- **Raw CSV download:** https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2019/2019-06-25/ufo_sightings.csv  
- **Approximate raw size:** ~14 MB (uncompressed)

