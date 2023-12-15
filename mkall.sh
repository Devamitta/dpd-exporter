#!/usr/bin/env bash

# export sbs-pd and ru to dictionary format from csv and write all output into .mkall-errors.txt

exec > >(tee "/home/deva/logs/mkall.log") 2>&1

cp "/home/deva/Documents/dpd-db/dps/csvs/dpd_dps_full.csv" "/home/deva/Documents/dps/spreadsheets/dpd_dps_full.csv"

cp "/home/deva/Documents/dpd-db/dps/csvs/dps_full.csv" "/home/deva/Documents/dps/spreadsheets/dps_full.csv"

poetry run python sbs_pd_filter.py

cd "../inflection"

echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
poetry run python "inflection generator.py"

# cd ../inflection-en

# poetry run python "inflection generator.py"

# echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"


cd "../exporter"

poetry run python exporter.py run-generate-html-and-json
poetry run python exporter.py run-generate-goldendict
# poetry run python exporter.py run-generate-html-and-json-dps-full
# poetry run python exporter.py run-generate-goldendict-dps-full
poetry run python exporter.py run-generate-html-and-json-sbs
poetry run python exporter.py run-generate-goldendict-sbs

echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

poetry run python unzip_dps.py

echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"


