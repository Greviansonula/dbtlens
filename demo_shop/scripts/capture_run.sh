#!/usr/bin/env bash
# Run from demo_shop/:  scripts/capture_run.sh <healthy|incident> <output_dir>
set -u
SCENARIO="$1"; OUT="$2"

python scripts/generate_data.py --scenario "$SCENARIO"
rm -rf target                      # start clean so no old files get mixed in
mkdir -p "$OUT"

dbt source freshness
cp target/sources.json "$OUT"/     # copy now, before the next command

dbt build
cp target/manifest.json target/run_results.json "$OUT"/
echo "saved $SCENARIO run to $OUT"