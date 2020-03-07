#!/bin/bash

HELICS_VERSION=$1

# Get HELICS apps for Linux
curl -O -L "https://github.com/GMLC-TDC/HELICS/releases/download/v${HELICS_VERSION}/Helics-${HELICS_VERSION}-Linux-x86_64.tar.gz"
tar xzf Helics-*.tar.gz && rm Helics-*.tar.gz && mv Helics-* helics || exit $?

# Add a copy of HELICS binaries to the data folder
cp helics/bin/helics_* helics_apps-pip/helics_apps/data/bin/

# Add lib64 to LD_LIBRARY_PATH so auditwheel can fix up the bdist wheel
LD_LIBRARY_PATH="$PWD/helics/lib64:$LD_LIBRARY_PATH"
export LD_LIBRARY_PATH

# Make sure pip and required tools are set up
pip install --upgrade pip
pip install setuptools wheel auditwheel

sudo apt-get install -y patchelf
