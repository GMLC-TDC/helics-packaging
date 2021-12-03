#!/bin/bash

DYLD_LIBRARY_PATH="$PWD/helics/lib:$PWD/helics/lib64:$DYLD_LIBRARY_PATH"
export DYLD_LIBRARY_PATH

# Ensure delocate and wheel are installed for fixing up wheels
python -m pip install --upgrade pip
pip install delocate wheel

# Bundle external shared libraries into the wheels
for whl in wheelhouse/*.whl; do
  newwhl="${whl%%macos*.whl}macosx_10_14_universal2.macosx_10_14_x86_64.macosx_11_0_arm64.whl"
  mv "$whl" "$newwhl"
  delocate-wheel -v "$newwhl" -w upload-wheelhouse
done
