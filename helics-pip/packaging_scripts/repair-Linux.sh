#!/bin/bash

# Get rid of second post in .post?.post. tag
for whl in wheelhouse/*.post*.post.*.whl; do
    mv "$whl" "${whl//\.post\./.}"
done

# Bundle external shared libraries into the wheels
for whl in wheelhouse/*.whl; do
  auditwheel repair "$whl" --plat manylinux2010_x86_64 -w wheelhouse/manylinux2010
done

