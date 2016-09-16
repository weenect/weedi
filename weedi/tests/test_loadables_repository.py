# -*- coding: utf-8 -*-

import unittest
try:
    import mock
except:
    import unittest.mock as mock

import weedi.loadables_repository as loadables_repository


class TestLoadablesRepository(unittest.TestCase):
    @mock.patch('weedi.loadables_repository.LoadablesRepository.load')
    def test_init_calls_load(self, mock_load):
        repository = loadables_repository.LoadablesRepository('config_file', None, 'error')
        repository = loadables_repository.LoadablesRepository('config_file', 'conf', 'error')
        mock_load.assert_called_once_with('config_file', 'conf', 'error')
