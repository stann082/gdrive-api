#!/usr/bin/env bash

pip install -e .
python -m pytest --cov-report=term --cov-report=xml --cov=. --cov-config=.coveragerc --cov-branch
