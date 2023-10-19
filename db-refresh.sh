#!/bin/sh

rm db.sqlite3
python manage.py migrate
python manage.py loaddata plants/fixtures/plants.json
python manage.py loaddata plants/fixtures/diseases.json