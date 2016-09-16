# -*- coding: utf-8 -*-

# =-
# (C)opyright Hareau SAS 2013-2016
#
# This is a Hareau SAS proprietary source code.
# Any reproduction modification or use without prior written
# approval from Hareau SAS is strictly forbidden.
# =-

import os
import sys

from setuptools import setup, find_packages

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')))

setup(
    name='project',
    version='0.1',
    author='Weenect',
    description='',
    license='proprietary',
    keywords='',
    url='',
    packages=find_packages(),
    include_package_data=True,
    install_requires=('weedi'),
    entry_points='''
        [services]
        database = project.services:Database
        mail = project.services:Mail
        manager = project.services:Manager
    ''',
    test_suite = "project.tests"
)
