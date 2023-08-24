#!/usr/bin/env bash

# export sbs-pd and ru to dictionary format from csv and write all output into .mkall-errors.txt

exec > >(tee "/home/deva/logs/mkall.log") 2>&1

poetry run python sbs_pd_filter.py

cd "../inflection"

echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
poetry run python "inflection generator.py"

cd ../inflection-en

poetry run python "inflection generator.py"

echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"


cd "../exporter"

poetry run python exporter.py run-generate-html-and-json
poetry run python exporter.py run-generate-goldendict
poetry run python exporter.py run-generate-html-and-json-sbs
poetry run python exporter.py run-generate-goldendict-sbs

echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

poetry run python unzip_dps.py

echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"


