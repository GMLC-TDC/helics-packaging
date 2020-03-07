#!/bin/bash

# Compile wheel with a recent version of python
pushd helics_apps-pip || exit $?
/opt/python/cp38-cp38/bin/python setup.py bdist_wheel --dist-dir=../wheelhouse
popd || exit $?

