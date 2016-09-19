# -*- coding: utf-8 -*-
#
# (c) 2016 Hareau SAS / Weenect, https://www.weenect.com
#
# This file is part of the weedi library
#
# MIT License : https://raw.githubusercontent.com/weenect/weedi/master/LICENSE.txt

import os

from setuptools import setup, find_packages

VERSION = '0.1'


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
  name='weedi',
  packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
  license="MIT",
  version=VERSION,
  description='A dependency injection system/container using setuptools entry points',
  long_description=read('README.rst'),
  author='Weenect',
  url='https://github.com/weenect/weedi',
  download_url='https://github.com/weenect/weedi/tarball/' + VERSION,
  keywords=['di', 'dependency injection', 'entry points', 'entry_points', 'setuptools'],
  requires=['configobj'],
  install_requires=['configobj'],
  tests_require=['mock'],
  extras_require={'test': ['mock']},
  setup_requires=['setuptools-pep8'],
  test_suite="weedi.tests",
  classifiers=[
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Topic :: Software Development :: Libraries :: Application Frameworks"
  ]
)
