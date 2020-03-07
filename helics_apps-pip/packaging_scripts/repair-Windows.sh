#!/bin/bash

pushd wheelhouse
mkdir upload-wheelhouse
popd

# Install wheel module for fixing up the wheels
python -m pip install --upgrade pip
python -m pip install wheel

# Bundle external shared libraries
for whl in $PWD/wheelhouse/*.whl; do
  mkdir tmp_dir
  pushd tmp_dir
  wheel unpack "$whl"
  #cp ../helics/bin/libzmq*.dll helics-*/helics
  wheel pack helics_apps-*/ --dest-dir=../upload-wheelhouse
  popd
  rm -rf tmp_dir
done

