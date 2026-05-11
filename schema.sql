DROP TABLE IF EXISTS ufo_sightings;

CREATE TABLE ufo_sightings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_time TEXT,                 -- stored as ISO 8601 string (YYYY-MM-DD HH:MM:SS)
    city_area TEXT,
    state TEXT,
    country TEXT,
    ufo_shape TEXT,
    encounter_length REAL,
    described_encounter_length TEXT,
    description TEXT,
    date_documented TEXT,
    latitude REAL,
    longitude REAL
);

-- Indexes are created after ingestion for faster load.