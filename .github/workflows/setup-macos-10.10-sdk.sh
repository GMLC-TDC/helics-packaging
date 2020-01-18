#!/bin/bash

XCODE_MACOS_PLATFORM_PATH="/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform"
XCODE_MACOS_SDK_PATH="${XCODE_MACOS_PLATFORM_PATH}/Developer/SDKs"

# Download macOS 10.10 SDK
wget https://github.com/phracker/MacOSX-SDKs/releases/download/10.13/MacOSX10.10.sdk.tar.xz

# Extract macOS 10.10 SDK to the XCode macOS SDKs folder
tar -xf MacOSX10.10.sdk.tar.xz -C "${XCODE_MACOS_SDK_PATH}"

# Set the MinimumSDKVersion for XCode to 10.10
/usr/libexec/PlistBuddy -c "Set :MinimumSDKVersion 10.10" "${XCODE_MACOS_PLATFORM_PATH}/Info.plist"

# Set MACOSX_DEPLOYMENT_TARGET on GitHub Actions
echo "::set-env name=MACOSX_DEPLOYMENT_TARGET::10.10"
