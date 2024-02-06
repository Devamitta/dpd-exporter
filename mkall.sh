#!/usr/bin/env bash

# export sbs-pd and ru to dictionary format from csv and write all output into .mkall-errors.txt

# exec > >(tee "/home/deva/logs/mkall.log") 2>&1

# cd "/home/deva/Documents/dpd-db"

# poetry run python dps/scripts/dps_csv.py

# cp "/home/deva/Documents/dpd-db/dps/csvs/dpd_dps_full.csv" "/home/deva/Documents/dps/spreadsheets/dpd_dps_full.csv"

cp "/home/deva/Documents/dpd-db/dps/csvs/dps_full.csv" "/home/deva/Documents/dps/spreadsheets/dps_full.csv"

cp "/home/deva/Documents/dpd-db/inflections/inflection_templates.xlsx" "/home/deva/Documents/dps/inflection/declensions & conjugations.xlsx"

poetry run python sbs_pd_filter.py

cd "../inflection"

echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
poetry run python "inflection generator.py"

# cd ../inflection-en

# poetry run python "inflection generator.py"

# echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"


cd "../exporter"

# ru
poetry run python exporter.py run-generate-html-and-json
poetry run python exporter.py run-generate-goldendict
# dps
poetry run python exporter.py run-generate-html-and-json-dps
poetry run python exporter.py run-generate-goldendict-dps
# sbs
poetry run python exporter.py run-generate-html-and-json-sbs
poetry run python exporter.py run-generate-goldendict-sbs

echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

poetry run python unzip_dps.py

echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"


