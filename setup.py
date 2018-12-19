import errno
import os
import platform
import site
from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext
from distutils.errors import DistutilsPlatformError
from distutils import sysconfig

import subprocess

class build_ext_with_protpbuf(build_ext):
    def run(self):
        try:
            proc = subprocess.Popen(
                ['protoc', '--cpp_out', 'imposm/parser/pbf/', 'osm.proto'],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except OSError as ex:
            if ex.errno == errno.ENOENT:
                print ("Could not find protoc command. Make sure protobuf is "
                    "installed and your PATH environment is set.")
                raise DistutilsPlatformError("Failed to generate protbuf "
                    "CPP files with protoc.")
            else:
                raise
        out = proc.communicate()[0]
        result = proc.wait()
        if result != 0:
            print("Error during protbuf files generation with protoc:")
            print(out)
            raise DistutilsPlatformError("Failed to generate protbuf "
                "CPP files with protoc.")
        build_ext.run(self)


install_requires = ['py3c']
if tuple(map(str, platform.python_version_tuple())) < ('2', '6'):
    install_requires.append('multiprocessing>=2.6')
if tuple(map(str, platform.python_version_tuple())) < ('3', '0'):
    install_requires.append('future>=0.17')

include_dirs = []
venv_include_dir = os.path.join(sysconfig.PREFIX, 'include', 'site', 'python' + sysconfig.get_python_version())
if os.path.exists(venv_include_dir):
    include_dirs.append(venv_include_dir)

setup(
    name='imposm.parser',
    version="1.0.8a",
    description='Fast and easy OpenStreetMap XML/PBF parser.',
    long_description=open('README.rst').read() + open('CHANGES').read(),
    author='Oliver Tonnhofer',
    author_email='olt@omniscale.de',
    url='http://imposm.org/docs/imposm.parser/latest/',
    license='Apache Software License 2.0',
    packages=find_packages(),
    namespace_packages = ['imposm'],
    include_package_data=True,
    package_data = {'': ['*.xml', '*.osm', '*.osm.bz2']},
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: C",
        "Programming Language :: C++",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    ext_modules=[
        Extension("imposm.parser.pbf.OSMPBF",
                  ["imposm/parser/pbf/osm.cc", "imposm/parser/pbf/osm.pb.cc"], libraries=['protobuf'], include_dirs=include_dirs),
    ],
    cmdclass={'build_ext':build_ext_with_protpbuf},
)
