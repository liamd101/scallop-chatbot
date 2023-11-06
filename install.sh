#!/bin/bash
python3 -m venv .env
source .env/bin/activate
pip install maturin
git clone git@github.com:liby99/scallop-v2.git
cd scallop-v2/
git checkout pdf-reader
make develop-scallop develop-scallopy develop-scallopy-ext develop-scallopy-plugins
cd ..
