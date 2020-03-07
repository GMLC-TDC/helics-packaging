#!/bin/bash

HELICS_VERSION=$1

# Get HELICS apps for macOS
curl -O -L "https://github.com/GMLC-TDC/HELICS/releases/download/v${HELICS_VERSION}/Helics-${HELICS_VERSION}-macOS-x86_64.zip"
unzip Helics-*.zip && rm Helics-*.zip && mv Helics-* helics || exit $?

# Add a copy of HELICS binaries to the data folder
cp helics/bin/helics_* helics_apps-pip/helics_apps/data/bin/

# Make sure pip and required tools are set up
pip install --upgrade pip
pip install setuptools wheel

# Set the DYLD_LIBRARY_PATH in GitHub Actions so delocate can fix up the wheel
DYLD_LIBRARY_PATH="${PWD}/helics/lib:${PWD}/helics/lib64:$DYLD_LIBRARY_PATH"
export DYLD_LIBRARY_PATH
echo "::set-env name=DYLD_LIBRARY_PATH::$PWD/helics/lib:$PWD/helics/lib64:$DYLD_LIBRARY_PATH"

