#!/bin/bash

PLAT_NAME=$1

# Create the wheel
pushd helics_apps-pip || exit $?
python setup.py bdist_wheel --plat-name="$PLAT_NAME" --dist-dir=../wheelhouse
popd || exit $?
