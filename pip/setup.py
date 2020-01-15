import os
import sys
import struct
import platform
import subprocess

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
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
        cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
                      '-DCMAKE_BUILD_WITH_INSTALL_RPATH=ON',
                      # For using the new Python find in CMake should set Python3_ROOT_DIR to os.path.split(os.path.dirname(os.path.abspath(sys.executable)))[0]
                      '-DPYTHON_EXECUTABLE=' + sys.executable,
                     ]

        # Use SWIG if it is available
        if _have_swig():
            cmake_args += ['-DHELICS_ENABLE_SWIG=ON']
        else:
            cmake_args += ['-DHELICS_ENABLE_SWIG=OFF']

        # CMake build type
        if self.debug:
            bldcfg = 'Debug'
        else:
            bldcfg = 'Release'
        build_args = ['--config', bldcfg]

        if platform.system() == "Windows":
            cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(bldcfg.upper(), extdir)]
            if struct.calcsize('P') == 8:
                cmake_args += ['-A', 'x64']
        else:
            cmake_args += ['-DCMAKE_BUILD_TYPE=' + bldcfg]

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        # Run CMake and build the helics python extension
        subprocess.check_call(['cmake', ext.sourcedir] + cmake_args, cwd=self.build_temp)
        subprocess.check_call(['cmake', '--build', '.'], cwd=self.build_temp)

        # Include the helics.py file in the module
        if not os.path.exists(helicsdir):
            os.makedirs(helicsdir)
        copyfile(os.path.join(self.build_temp, 'helics.py'), os.path.join(extdir, 'helics.py'))

setup(
    name='helics_test',
    version='2.3.1',
    author='GMLC-TDC',
    author_email='helicsdevelopers@helics.org',
    maintainer='',
    maintainer_email='',
    url="https://github.com/GMLC-TDC/HELICS",
    download_url="https://github.com/GMLC-TDC/HELICS/releases",
    license='BSD',
    keywords='co-simulation',
    description='Hierarchical Engine for Large-scale Infrastructure Co-Simulation (HELICS)',
    long_description='',
    ext_modules=[HelicsExtension('cmake_example', sourcedir='src/interfaces/python')],
    cmdclass=dict(build_ext=HelicsBuild),
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
