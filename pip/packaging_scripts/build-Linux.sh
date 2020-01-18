#!/bin/bash

# Compile wheels
pushd pip
for PYBIN in /opt/python/cp3*/bin; do
  "${PYBIN}/python" setup.py bdist_wheel --dist-dir=../wheelhouse
done
popd

