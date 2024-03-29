#!/bin/bash

HELICS_VERSION=$1
WINARCH=$2

# Install HELICS shared library for Windows
curl -O -L "https://github.com/GMLC-TDC/HELICS/releases/download/v${HELICS_VERSION}/Helics-shared-${HELICS_VERSION}-${WINARCH}.tar.gz"
tar xzf Helics-*.tar.gz && rm Helics-*.tar.gz && mv Helics-* helics || exit $?

# Add a copy of HELICS to the bundled folder for building the Python wheel
mkdir -p helics-pip/bundled/helics
curl -O -L "https://github.com/GMLC-TDC/HELICS/releases/download/v${HELICS_VERSION}/Helics-v${HELICS_VERSION}-source.tar.gz" || exit $?
tar xzf Helics-*.tar.gz -C helics-pip/bundled/helics/ && rm Helics-*.tar.gz || exit $?

mkdir wheelhouse

# Set the CMAKE_PREFIX_PATH environment variable in GitHub Actions
CMAKE_PREFIX_PATH="${PWD}/helics"
export CMAKE_PREFIX_PATH
echo "CMAKE_PREFIX_PATH=${PWD}/helics" >> $GITHUB_ENV

# Copy any patched files to the HELICS source tree if they exist
cp -r helics-pip/patches/${HELICS_VERSION}/* helics-pip/bundled/helics/ || true
