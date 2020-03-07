#!/bin/bash

# Compile wheel with a recent version of python
pushd helics_apps-pip || exit $?
/opt/cp37/bin/python setup.py bdist_wheel --dist-dir=../wheelhouse
popd || exit $?

