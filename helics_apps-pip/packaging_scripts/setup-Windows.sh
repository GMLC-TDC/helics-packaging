#!/bin/bash

HELICS_VERSION=$1
WINARCH=$2

# Get HELICS apps for Windows
curl -O -L "https://github.com/GMLC-TDC/HELICS/releases/download/v${HELICS_VERSION}/Helics-${HELICS_VERSION}-${WINARCH}.zip"
unzip Helics-*.zip && rm Helics-*.zip && mv Helics-* helics || exit $?

# Add a copy of HELICS binaries to the data folder
cp helics/bin/helics_* helics_apps-pip/helics_apps/data/bin/

# Make sure pip and required tools are set up
pip install --upgrade pip
pip install setuptools wheel

mkdir wheelhouse

