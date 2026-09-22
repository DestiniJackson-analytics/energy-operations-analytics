from pathlib import Path

import duckdb


project_root = Path(__file__).resolve().parents[1]
raw_data_path = project_root / "data" / "raw" / "nyc_building_energy.csv"
schema_output_path = project_root / "docs" / "raw_schema.csv"

if not raw_data_path.exists():
    raise FileNotFoundError(
        "Raw dataset not found. Run src/download_data.py first."
    )

connection = duckdb.connect()

safe_data_path = str(raw_data_path).replace("'", "''")

connection.execute(
    f"""
    CREATE OR REPLACE VIEW raw_energy AS
    SELECT *
    FROM read_csv(
        '{safe_data_path}',
        header = true,
        all_varchar = true,
        ignore_errors = true
    )
    """
)

row_count = connection.execute(
    "SELECT COUNT(*) FROM raw_energy"
).fetchone()[0]

schema = connection.execute(
    "DESCRIBE raw_energy"
).fetchdf()

schema.insert(
    0,
    "column_position",
    range(1, len(schema) + 1),
)

schema.to_csv(schema_output_path, index=False)

print(f"Row count: {row_count:,}")
print(f"Column count: {len(schema):,}")
print(f"Schema saved to: {schema_output_path}")

print("\nFirst 30 columns:")
print(
    schema[
        ["column_position", "column_name"]
    ].head(30).to_string(index=False)
)

connection.close()