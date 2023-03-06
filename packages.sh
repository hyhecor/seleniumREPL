#!/bin/bash
python3 -m venv .venv

source ./.venv/bin/activate

python3 -m pip install -U pip
python3 -m pip install -U selenium==4.8.2