#!/bin/bash

#SBATCH --job-name=nobr_svc_syp
#SBATCH --output=svc.out
#SBATCH --cpus-per-task=10
#SBATCH --gres=gpu
#SBATCH --partition=brown

curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
source ~/.poetry/env
