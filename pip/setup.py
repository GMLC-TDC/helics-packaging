import io
import os
import sys
import struct
import platform
import subprocess
import versioneer

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from distutils import sysconfig
from shutil import copyfile

class HelicsExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)

def _have_swig():
    try:
        subprocess.check_call(['swig', '-version'])
    except OSError:
        return False
    else:
        return True

def _is_vs_cmake_default():
    try:
        cmake_help_output=subprocess.check_output(['cmake', '--help'])
    except OSError:
        return False
    else:
        return '* Visual Studio' in str(cmake_help_output)

class HelicsBuild(build_ext):
    def run(self):
        try:
            subprocess.check_call(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake must be installed to build the HELICS extension")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        if not isinstance(ext, HelicsExtension):
            super().build_extension(ext)
            return

        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        helicsdir = os.path.abspath(os.path.join(extdir, 'helics'))
        cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + helicsdir,
                      '-DCMAKE_BUILD_WITH_INSTALL_RPATH=ON',
                      # For using the new Python find in CMake should set Python3_ROOT_DIR to os.path.split(os.path.dirname(os.path.abspath(sys.executable)))[0]
                      # the CMake FindPython module will likely need changes to support static mode Python interpreters
                      # https://github.com/pypa/manylinux/issues/30 and https://github.com/pypa/manylinux/issues/255
                      #'-DHELICS_USE_NEW_PYTHON_FIND=ON',
                      #'-DPython3_EXECUTABLE=' + sys.executable,
                      #'-DPython3_INCLUDE_DIR=' + sysconfig.get_python_inc(plat_specific=True),
                      #'-DPython3_LIBRARY_RELEASE=/',
                      #'-DPython3_LIBRARY_DEBUG=/',
                     ]

        # This is a hack to get around CMake only working with Python interpreters compiled with --enable-shared
        # Basically Linux+macOS don't require a library to link to, but Windows always requires linking to a library
        # Weird thing: on Windows with multiple installs, setting the Python executable can make it find an incorrect library
        if platform.system() != "Windows":
            cmake_args += ['-DPYTHON_EXECUTABLE=' + sys.executable,
                           '-DPYTHON_LIBRARY=' + os.path.join(sysconfig.get_python_lib(plat_specific=True, standard_lib=True)),
                           '-DPYTHON_INCLUDE_DIR=' + sysconfig.get_python_inc(plat_specific=True),
                          ]
        #else:
        #    cmake_args += ['-DPYTHON_LIBRARY=' + os.path.join(os.path.dirname(sys.executable), 'libs', 'python38.lib'),
        #                   '-DPYTHON_INCLUDE_DIR=' + sysconfig.get_python_inc(plat_specific=True),
        #                  ]

        # Add the Python 2 flag for building a Python 2 compatible swig module
        if sys.version_info[0] == 2:
            cmake_args += ['-DBUILD_PYTHON2_INTERFACE=ON']

        # Use SWIG if it is available
        if _have_swig():
            cmake_args += ['-DHELICS_ENABLE_SWIG=ON']
        else:
            cmake_args += ['-DHELICS_ENABLE_SWIG=OFF']

        # CMake build type
        if self.debug:
            bldcfg = 'Release'
        else:
            bldcfg = 'Release'
        build_args = ['--config', bldcfg]

        # Check if the environment/user set a CMake generator
        user_set_cmake_gen = 'CMAKE_GENERATOR' in os.environ
        
        if platform.system() == "Windows" and ((not user_set_cmake_gen and _is_vs_cmake_default()) or (user_set_cmake_gen and 'Visual Studio' in os.environ.get('CMAKE_GENERATOR'))):
            print("Using VS")
            cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(bldcfg.upper(), helicsdir)]
            if struct.calcsize('P') == 8:
                cmake_args += ['-A', 'x64']
            else:
                cmake_args += ['-A', 'Win32']
        else:
            cmake_args += ['-DCMAKE_BUILD_TYPE=' + bldcfg]

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        # Run CMake and build the helics python extension
        subprocess.check_call(['cmake', ext.sourcedir] + cmake_args, cwd=self.build_temp)
        subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=self.build_temp)

        # Include the helics.py file in the module
        if not os.path.exists(helicsdir):
            os.makedirs(helicsdir)
        copyfile(os.path.join(self.build_temp, 'helics.py'), os.path.join(helicsdir, 'helics.py'))

# Get the directory setup.py is located in
setup_py_dir = os.path.abspath(os.path.dirname(__file__))

# Get the README.md contents
README_contents = io.open(os.path.join(setup_py_dir, 'README.md'), encoding="utf-8").read()

# Use versioneer to get the version tag
PKG_VERSION = versioneer.get_version()

# Try getting a version from PKG-INFO if this is a build from an sdist package
if PKG_VERSION == "0+unknown":
    try:
        with open(os.path.join(setup_py_dir, 'PKG-INFO')) as f:
            for line in f:
                if line.startswith("Version:"):
                    PKG_VERSION=line[8:].strip()
    except IOError:
        print("Unable to get a package version, using 0+unknown")

setup(
    name='helics',
    version=PKG_VERSION,
    author='GMLC-TDC',
    author_email='helicsdevelopers@helics.org',
    maintainer='',
    maintainer_email='',
    url="https://github.com/GMLC-TDC/HELICS",
    download_url="https://github.com/GMLC-TDC/HELICS/releases",
    license='BSD',
    keywords='co-simulation',
    description='Hierarchical Engine for Large-scale Infrastructure Co-Simulation (HELICS)',
    long_description=README_contents,
    long_description_content_type='text/markdown',
    packages=['helics'],
    ext_modules=[HelicsExtension('helics', sourcedir='bundled/helics/interfaces/python')],
    cmdclass={
        'build_ext': HelicsBuild,
        'versioneer': versioneer.get_cmdclass()
    },
    entry_points={
        'console_scripts': [
        ]
    },
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Unix",
        "Programming Language :: C",
        "Programming Language :: C++",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries",
        "Topic :: Scientific/Engineering",
    ],
)
