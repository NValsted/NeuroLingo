#!/bin/bash

#SBATCH --job-name=nobr_svc_syp
#SBATCH --output=svc.out
#SBATCH --cpus-per-task=10
#SBATCH --gres=gpu
#SBATCH --time=00:05:00
#SBATCH --partition=brown
#SBATCH --mail-type=FAIL, END

curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
source ~/.poetry/env
cd neurolingo/
poetry install
cd bin/
python script.py
