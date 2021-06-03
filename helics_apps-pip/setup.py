# -*- coding: utf-8 -*-
import io
import os
import versioneer

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import subprocess
import sys
import re
import tarfile
import platform
import shlex
from wheel.bdist_wheel import bdist_wheel

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

# Get the directory setup.py is located in
setup_py_dir = os.path.abspath(os.path.dirname(__file__))

# Get the README.md contents
README_contents = io.open(os.path.join(setup_py_dir, "README.md"), encoding="utf-8").read()

HELICS_SOURCE = os.path.join(setup_py_dir, "./_source")
HELICS_VERSION = versioneer.get_version()
HELICS_VERSION = re.findall(r"(?:(\d+\.(?:\d+\.)*\d+))", HELICS_VERSION)[0]
HELICS_INSTALL = os.path.join(setup_py_dir, "./helics_apps/data")
DOWNLOAD_URL = "https://github.com/GMLC-TDC/HELICS/releases/download/v{version}/Helics-v{version}-source.tar.gz".format(version=HELICS_VERSION)


class HELICSBdistWheel(bdist_wheel):
    def get_tag(self):
        rv = super().get_tag()
        return ("py2.py3", "none",) + rv[2:]


class HELICSCMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(["cmake", "--version"])
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: " + ", ".join(e.name for e in self.extensions))

        cmake_version = re.search(r"version\s*([\d.]+)", out.decode().lower()).group(1)
        cmake_version = [int(i) for i in cmake_version.split(".")]
        if cmake_version < [3, 5, 1]:
            raise RuntimeError("CMake >= 3.5.1 is required to build helics")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):

        self.helics_url = DOWNLOAD_URL
        self.helics_source = HELICS_SOURCE

        if os.path.exists(HELICS_INSTALL) and sum(len(files) for _, _, files in os.walk(HELICS_INSTALL)) > 2:
            return

        print("Opening", self.helics_url)
        r = urlopen(self.helics_url)

        if r.getcode() == 200:
            content = io.BytesIO(r.read())
            content.seek(0)
            with tarfile.open(fileobj=content) as tf:
                tf.extractall(self.helics_source)
        else:
            return

        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        extdir = os.path.join(extdir, "helics_apps", "data")
        # required for auto - detection of auxiliary "native" libs
        if not extdir.endswith(os.path.sep):
            extdir += os.path.sep

        cmake_args = [
            "-DHELICS_DISABLE_GIT_OPERATIONS=OFF",
            "-DHELICS_ZMQ_SUBPROJECT=ON",
            "-DCMAKE_BUILD_TYPE=Release",
            "-DCMAKE_INSTALL_PREFIX={}".format(extdir),
            # "-DCMAKE_RUNTIME_OUTPUT_DIRECTORY={}".format(os.path.join(extdir, "bin")),
            # "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={}".format(os.path.join(extdir, "lib")),
        ]

        cfg = "Debug" if self.debug else "Release"
        build_args = ["--config", cfg]

        if platform.system() == "Windows":
            cmake_args += ["-DCMAKE_RUNTIME_OUTPUT_DIRECTORY_{}={}".format(cfg.upper(), extdir)]
            if sys.maxsize > 2 ** 32:
                cmake_args += ["-A", "x64"]
                build_args += ["--", "/m"]
        else:
            cmake_args += ["-DCMAKE_BUILD_TYPE=" + cfg]
            build_args += ["--", "-j"]

        env = os.environ.copy()
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call(["cmake", ext.sourcedir] + cmake_args, cwd=self.build_temp, env=env)
        cmd = " ".join(["cmake", "--build", ".", "--target", "install"] + build_args)
        print(cmd)
        subprocess.check_call(shlex.split(cmd), cwd=self.build_temp)


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=HELICS_SOURCE):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = sourcedir


cmdclass = {"build_ext": HELICSCMakeBuild, "bdist_wheel": HELICSBdistWheel}


for k, v in versioneer.get_cmdclass().items():
    cmdclass[k] = v

setup(
    name="helics_apps",
    version=versioneer.get_version(),
    author="GMLC-TDC",
    author_email="helicsdevelopers@helics.org",
    maintainer="",
    maintainer_email="",
    url="https://github.com/GMLC-TDC/HELICS",
    download_url="https://github.com/GMLC-TDC/HELICS/releases",
    license="BSD",
    keywords="helics co-simulation",
    description="Hierarchical Engine for Large-scale Infrastructure Co-Simulation (HELICS)",
    long_description=README_contents,
    long_description_content_type="text/markdown",
    packages=["helics_apps"],
    package_data={"helics_apps": ["data/*"]},
    include_package_data=True,
    ext_modules=[CMakeExtension("helics")],
    cmdclass=cmdclass,
    entry_points={
        "console_scripts": [
            "helics_app=helics_apps:helics_app",
            "helics_broker=helics_apps:helics_broker",
            "helics_broker_server=helics_apps:helics_broker_server",
            "helics_player=helics_apps:helics_player",
            "helics_recorder=helics_apps:helics_recorder",
        ]
    },
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Unix",
        "Programming Language :: C",
        "Programming Language :: C++",
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Scientific/Engineering",
        "Topic :: Utilities",
    ],
)
