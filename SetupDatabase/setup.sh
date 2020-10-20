#!/bin/bash
## the SQL setup script must be run as admin in postgres first. ElasticSearch should be configured for system in setup_elasticsearch.py
python3 ../setup_DB/add_companies.py
python3 ../setup_DB/add_congresspeople.py
python3 ../setup_DB/add_congresspeople.py
python3 ../setup_DB/add_countries.py
python3 ../setup_DB/setup_elasticsearch.py
