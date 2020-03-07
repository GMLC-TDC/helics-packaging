#!/bin/bash

DYLD_LIBRARY_PATH="$PWD/helics/lib:$PWD/helics/lib64:$DYLD_LIBRARY_PATH"
export DYLD_LIBRARY_PATH

# Ensure delocate and wheel are installed for fixing up wheels
python -m pip install --upgrade pip
pip install delocate wheel

# Bundle external shared libraries into the wheels
for whl in wheelhouse/*.whl; do
  delocate-wheel -v "$whl" -w upload-wheelhouse
done
