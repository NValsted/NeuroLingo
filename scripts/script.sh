#!/bin/bash

cd ../ && \
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - && \
source ~/.poetry/env && \
poetry install && \
cd ./bin/ \
python script.py
