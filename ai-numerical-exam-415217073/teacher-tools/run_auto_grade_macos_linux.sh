#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 auto_grade.py --project . --output auto-assessment.json
