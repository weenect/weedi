# -*- coding: utf-8 -*-
#
# (c) 2016 Hareau SAS / Weenect, https://www.weenect.com
#
# This file is part of the weedi library
#
# MIT License : https://raw.githubusercontent.com/weenect/weedi/master/LICENSE.txt

import unittest

import weedi.loadable as loadable


class TestLoadable(unittest.TestCase):
    def test_class_attribute(self):
        """ Useless test. Created to quickly set up test suite """
        self.assertEqual(loadable.Loadable.load_priority, 0)
        self.assertEqual(loadable.Loadable.spec, {})
