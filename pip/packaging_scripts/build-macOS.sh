#!/bin/bash

export CMAKE_PREFIX_PATH

python -m pip install --upgrade pip
pip install setuptools wheel

# Compile wheels
pushd pip
python setup.py bdist_wheel --dist-dir=../wheelhouse
popd
