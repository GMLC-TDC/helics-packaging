#!/bin/bash

# Bundle external shared libraries into the wheel
for whl in wheelhouse/*.whl; do
  python -m auditwheel repair "$whl" --plat manylinux2010_x86_64 -w wheelhouse/manylinux2010
done

