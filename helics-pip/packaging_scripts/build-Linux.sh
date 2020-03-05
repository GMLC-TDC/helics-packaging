#!/bin/bash

# Compile wheels
pushd helics-pip || exit $?
for PYBIN in /opt/python/cp3*/bin; do
  "${PYBIN}/python" setup.py bdist_wheel --dist-dir=../wheelhouse
done

PATH="$HOME/swig-install/bin:$PATH"
for PYBIN in /opt/python/cp2*/bin; do
  "${PYBIN}/python" setup.py bdist_wheel --dist-dir=../wheelhouse
done
popd || exit $?

