#!/bin/bash

# Create the wheel
pushd helics_apps-pip || exit $?
python setup.py bdist_wheel --dist-dir=../wheelhouse --verbose
popd || exit $?

