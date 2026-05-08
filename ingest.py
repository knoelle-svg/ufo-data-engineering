import pandas as pd
import sqlite3

# 1. URL of the UFO dataset (raw CSV file)
UFO_DATA_URL = (
    "https://raw.githubusercontent.com/"
    "rfordatascience/tidytuesday/"
    "2e9bd5a67e09b14d01f616b00f7f7e0931515d24/"
    "data/2019/2019-06-25/ufo_sightings.csv"
)

# 2. Download the CSV into a pandas DataFrame
print("Downloading UFO data...")
df = pd.read_csv(UFO_DATA_URL)
print(f"Downloaded {len(df)} rows")

# 3. Create (or connect to) a SQLite database
print("Creating SQLite database...")
conn = sqlite3.connect("ufo.db")

# 4. Load the data into a table called 'ufo_sightings'
df.to_sql(
    "ufo_sightings",
    conn,
    if_exists="replace",
    index=False
)

# 5. Close the database connection
conn.close()

print("Ingestion complete. Database saved as ufo.db")