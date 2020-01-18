#!/bin/bash

export CMAKE_PREFIX_PATH

python -m pip install --upgrade pip
python -m pip install setuptools wheel

# Compile wheels
cd pip
python setup.py bdist_wheel --dist-dir=../wheelhouse

