#!/bin/bash

DYLD_LIBRARY_PATH="$PWD/helics/lib:$PWD/helics/lib64:$DYLD_LIBRARY_PATH"
export DYLD_LIBRARY_PATH

python -m pip install --upgrade pip
pip install delocate

# Get rid of second post in .post?.post. tag
for whl in wheelhouse/*.post*.post.*.whl; do
    mv "$whl" "${whl//\.post\./.}"
done

# Bundle external shared libraries into the wheels
for whl in wheelhouse/*.whl; do
  delocate-wheel -v "$whl" -w wheelhouse/fixed-wheels
done

# Set the macOS version to match the SDK built with, and work with system/Python.org installs
# See https://github.com/MacPython/wiki/wiki/Spinning-wheels#lying-about-your-wheel-compability
for f in wheelhouse/fixed-wheels/*-macosx_10_13_x86_64.whl; do
  mv "$f" "${f%_10_13_x86_64.whl}_10_9_intel.whl"
done
