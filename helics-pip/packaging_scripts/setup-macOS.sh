#!/bin/bash

HELICS_VERSION=$1

# Install HELICS shared library for macOS
curl -O -L "https://github.com/GMLC-TDC/HELICS/releases/download/v${HELICS_VERSION}/Helics-shared-${HELICS_VERSION}-macOS-x86_64.tar.gz"
tar xzf Helics-*.tar.gz && rm Helics-*.tar.gz && mv Helics-* helics || exit $?

# Add a copy of HELICS to the bundled folder for building the Python wheel
mkdir -p helics-pip/bundled/helics
curl -O -L "https://github.com/GMLC-TDC/HELICS/releases/download/v${HELICS_VERSION}/Helics-v${HELICS_VERSION}-source.tar.gz" || exit $?
tar xzf Helics-*.tar.gz -C helics-pip/bundled/helics/ && rm Helics-*.tar.gz || exit $?

# Set the CMAKE_PREFIX_PATH environment variable in GitHub Actions
CMAKE_PREFIX_PATH="${PWD}/helics"
export CMAKE_PREFIX_PATH
echo "::set-env name=CMAKE_PREFIX_PATH::${PWD}/helics"

# Set the DYLD_LIBRARY_PATH in GitHub Actions so delocate can fix up the wheels
DYLD_LIBRARY_PATH="${PWD}/helics/lib:${PWD}/helics/lib64:$DYLD_LIBRARY_PATH"
export DYLD_LIBRARY_PATH
echo "::set-env name=DYLD_LIBRARY_PATH::$PWD/helics/lib:$PWD/helics/lib64:$DYLD_LIBRARY_PATH"

