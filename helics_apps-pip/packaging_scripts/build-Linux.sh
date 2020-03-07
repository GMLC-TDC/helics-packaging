#!/bin/bash

# Create the wheel
pushd helics_apps-pip || exit $?
/opt/python/cp37-cp37m/bin/python setup.py bdist_wheel --dist-dir=../wheelhouse --verbose
popd || exit $?

