# BSD 3-Clause License; see https://github.com/jpivarski/awkward-1.0/blob/master/LICENSE

import glob
import os
import platform
import subprocess
import sys
import distutils.util

import setuptools.command.build_ext
import setuptools.command.install

from setuptools import setup, Extension

if platform.system() == "Windows":
    print("awkward1_cuda is not supported on Windows")
    exit(1)

class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=""):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)

class CMakeBuild(setuptools.command.build_ext.build_ext):
    def build_extensions(self):
        try:
            out = subprocess.check_output(["cmake", "--version"])
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: " + ", ".join(x.name for x in self.extensions))

        for x in self.extensions:
            self.build_extension(x)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        cmake_args = ["-DCMAKE_INSTALL_PREFIX={0}".format(extdir),
                      "-DCMAKE_OSX_DEPLOYMENT_TARGET=10.9"]
        try:
            compiler_path = self.compiler.compiler_cxx[0]
            cmake_args.append("-DCMAKE_CXX_COMPILER={0}".format(compiler_path))
        except AttributeError:
            print("Not able to access compiler path (on Windows), using CMake default")


        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        build_dir = self.build_temp

        # for scikit-build:
        # build_dir = os.path.join(DIR, "_pybuild")

        subprocess.check_call(["cmake", "-S", ext.sourcedir, "-B", build_dir] + cmake_args)
        subprocess.check_call(["cmake", "--build", build_dir])
        subprocess.check_call(["cmake", "--build", build_dir, "--target", "install"])

if platform.system() == "Windows":
    print("awkward1_cuda is not supported on Windows")
    exit(1)
else:
    # Libraries do not exist yet, so they cannot be determined with a glob pattern.
    libdir = os.path.join(os.path.join("build", "lib.%s-%d.%d" % (distutils.util.get_platform(), sys.version_info[0], sys.version_info[1])), "awkward1")
    static = ".a"
    if platform.system() == "Darwin":
        shared = ".dylib"
    else:
        shared = ".so"
    libraries = [("lib", [os.path.join(libdir, "libawkward-cuda-kernels-static" + static),
                          os.path.join(libdir, "libawkward-cuda-kernels" + shared)])]

    Install = setuptools.command.install.install

setup(name = "awkward1_cuda",
      packages = setuptools.find_packages(where="src"),
      package_dir = {"": "src"},
      include_package_data = True,
      package_data = {"": ["*.dll"]},
      data_files = libraries + [
          ("include/awkward",              glob.glob("include/awkward/*.h")),
          ("include/awkward/cuda-kernels", glob.glob("include/awkward/cuda-kernels/*.h"))],
      version = "0.0.1",
      author = "Jim Pivarski",
      author_email = "pivarski@princeton.edu",
      maintainer = "Jim Pivarski",
      maintainer_email = "pivarski@princeton.edu",
      description = "Development of awkward 1.0, to replace scikit-hep/awkward-array in 2020.",
      long_description = """<a href="https://github.com/scikit-hep/awkward-1.0#readme"><img src="https://github.com/scikit-hep/awkward-1.0/raw/master/docs-img/logo/logo-300px.png"></a>
Awkward Array is a library for **nested, variable-sized data**, including arbitrary-length lists, records, mixed types, and missing data, using **NumPy-like idioms**.

Arrays are **dynamically typed**, but operations on them are **compiled and fast**. Their behavior coincides with NumPy when array dimensions are regular and generalizes when they're not.

<table>
  <tr>
    <td width="33%" valign="top">
      <a href="https://awkward-array.org/how-to.html">
        <img src="https://github.com/scikit-hep/awkward-1.0/raw/master/docs-img/panel-data-analysts.png" width="268">
      </a>
      <p align="center"><b>
        <a href="https://awkward-array.org/how-to.html">
        How-to documentation<br>for data analysts
        </a>
      </b></p>
    </td>
    <td width="33%" valign="top">
      <a href="https://awkward-array.org/how-it-works.html">
        <img src="https://github.com/scikit-hep/awkward-1.0/raw/master/docs-img/panel-developers.png" width="268">
      </a>
      <p align="center"><b>
        <a href="https://awkward-array.org/how-it-works.html">
        How-it-works tutorials<br>for developers
        </a>
      </b></p>
    </td>
    <td width="33%" valign="top">
      <a href="https://awkward-array.readthedocs.io/en/latest/index.html">
        <img src="https://github.com/scikit-hep/awkward-1.0/raw/master/docs-img/panel-sphinx.png" width="268">
      </a>
      <p align="center"><b>
        <a href="https://awkward-array.readthedocs.io/en/latest/index.html">
        Python<br>API reference
        </a>
      </b></p>
      <a href="https://awkward-array.readthedocs.io/en/latest/_static/index.html">
        <img src="https://github.com/scikit-hep/awkward-1.0/raw/master/docs-img/panel-doxygen.png" width="268">
      </a>
      <p align="center"><b>
        <a href="https://awkward-array.readthedocs.io/en/latest/_static/index.html">
        C++<br>API reference
        </a>
      </b></p>
    </td>
  </tr>
</table>
""",
      long_description_content_type = "text/markdown",
      url = "https://github.com/scikit-hep/awkward-1.0",
      download_url = "https://github.com/scikit-hep/awkward-1.0/releases",
      license = "BSD 3-clause",
      python_requires = ">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",


      ext_modules = [CMakeExtension("awkward_cuda_kernels")], # NOT scikit-build
      cmdclass = {"build_ext": CMakeBuild,       # NOT scikit-build
                  "install": Install},

      classifiers = [
          #         "Development Status :: 1 - Planning",
                    "Development Status :: 2 - Pre-Alpha",
          #         "Development Status :: 3 - Alpha",
          #         "Development Status :: 4 - Beta",
          #         "Development Status :: 5 - Production/Stable",
          #         "Development Status :: 6 - Mature",
          #         "Development Status :: 7 - Inactive",
          "Intended Audience :: Developers",
          "Intended Audience :: Information Technology",
          "Intended Audience :: Science/Research",
          "License :: OSI Approved :: BSD License",
          "Operating System :: MacOS",
          "Operating System :: POSIX",
          "Operating System :: Unix",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Topic :: Scientific/Engineering",
          "Topic :: Scientific/Engineering :: Information Analysis",
          "Topic :: Scientific/Engineering :: Mathematics",
          "Topic :: Scientific/Engineering :: Physics",
          "Topic :: Software Development",
          "Topic :: Utilities",
      ])