# -*- coding: utf-8 -*-
#
# (c) 2016 Hareau SAS / Weenect, https://www.weenect.com
#
# This file is part of the weedi library
#
# MIT License : https://raw.githubusercontent.com/weenect/weedi/master/LICENSE.txt

from setuptools import setup, find_packages

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

        [services.missing]
        database = project.services:Database
        manager = project.services:Manager

        [services.configuration]
        config = project.services:ConfigurationNeededService

        [services.priority]
        database = project.services:DatabaseUnpriorized
        mail = project.services:Mail
        manager = project.services:Manager
    ''',
    test_suite = "project.tests"
)
