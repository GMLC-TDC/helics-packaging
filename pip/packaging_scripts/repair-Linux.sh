#!/bin/bash

# Bundle external shared libraries into the wheels
for whl in wheelhouse/*.whl; do
  auditwheel repair "$whl" --plat manylinux2010_x86_64 -w wheelhouse/manylinux2010
done

