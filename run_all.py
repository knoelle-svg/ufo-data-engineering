
"""
run_all.py

End-to-end entry point for the UFO Sightings data engineering exercise.

This script:
1. Downloads and ingests the raw dataset into SQLite
2. Executes all analysis queries and prints results

Usage:
    python run_all.py
"""

import subprocess
import sys


def run_step(script_name: str):
    print(f"\n--- Running {script_name} ---")
    result = subprocess.run(
        [sys.executable, script_name],
        check=True
    )
    return result


def main():
    run_step("ingest.py")
    run_step("analysis.py")
    print("\n✅ Pipeline completed successfully.")


if __name__ == "__main__":
    main()
