# -*- coding: utf-8 -*-

import unittest

import weedi.loadable as loadable


class TestLoadable(unittest.TestCase):
    def test_class_attribute(self):
        """ Useless test. Created to quickly set up test suite """
        self.assertEqual(loadable.Loadable.load_priority, 0)
        self.assertEqual(loadable.Loadable.spec, {})
