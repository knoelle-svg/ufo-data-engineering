CREATE TABLE IF NOT EXISTS ufo_sightings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_time TEXT,
    city TEXT,
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

CREATE INDEX IF NOT EXISTS idx_ufo_state ON ufo_sightings(state);
CREATE INDEX IF NOT EXISTS idx_ufo_country ON ufo_sightings(country);
CREATE INDEX IF NOT EXISTS idx_ufo_shape ON ufo_sightings(ufo_shape);
CREATE INDEX IF NOT EXISTS idx_ufo_date_time ON ufo_sightings(date_time);