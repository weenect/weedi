# -*- coding: utf-8 -*-
#
# (c) 2016 Hareau SAS / Weenect, https://www.weenect.com
#
# This file is part of the weedi library
#
# MIT License : https://raw.githubusercontent.com/weenect/weedi/master/LICENSE.txt

import os
import unittest

import weedi.exc

import project.repository as repository
import project.services as services


class TestServicesRepository(unittest.TestCase):
    def test_no_config_file(self):
        service_repository = repository.ServicesRepository()
        service_repository.load()

        self.assertIsInstance(service_repository['mail'], services.Mail)
        self.assertEqual(service_repository['mail'].host, "127.0.0.1")
        self.assertEqual(service_repository['mail'].port, 25)
        self.assertEqual(service_repository['mail'].timeout, 120.0)

        self.assertIsInstance(service_repository['database'], services.Database)
        self.assertEqual(service_repository['database'].host, "localhost")
        self.assertEqual(service_repository['database'].port, 3306)
        self.assertFalse(service_repository['database'].debug)

        self.assertIsInstance(service_repository['manager'], services.Manager)
        self.assertEqual(service_repository['manager'].db, service_repository['database'])
        self.assertEqual(service_repository['manager'].mail, service_repository['mail'])

    def test_no_config_file_overriden(self):
        service_repository = repository.ServicesRepository()
        service_repository.load(None, {'services': {'mail': {'host': 'smtp.local'}}})

        self.assertIsInstance(service_repository['mail'], services.Mail)
        self.assertEqual(service_repository['mail'].host, 'smtp.local')
        self.assertEqual(service_repository['mail'].port, 25)
        self.assertEqual(service_repository['mail'].timeout, 120.0)

        self.assertIsInstance(service_repository['database'], services.Database)
        self.assertEqual(service_repository['database'].host, "localhost")
        self.assertEqual(service_repository['database'].port, 3306)
        self.assertFalse(service_repository['database'].debug)

        self.assertIsInstance(service_repository['manager'], services.Manager)
        self.assertEqual(service_repository['manager'].db, service_repository['database'])
        self.assertEqual(service_repository['manager'].mail, service_repository['mail'])

    def test_with_config_file(self):
        service_repository = repository.ServicesRepository()
        service_repository.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.ini'))

        self.assertIsInstance(service_repository['mail'], services.Mail)
        self.assertEqual(service_repository['mail'].host, "8.8.8.8")
        self.assertEqual(service_repository['mail'].port, 52)
        self.assertEqual(service_repository['mail'].timeout, 300.0)

        self.assertIsInstance(service_repository['database'], services.Database)
        self.assertEqual(service_repository['database'].host, "database.local")
        self.assertEqual(service_repository['database'].port, 5432)
        self.assertTrue(service_repository['database'].debug)

        self.assertIsInstance(service_repository['manager'], services.Manager)
        self.assertEqual(service_repository['manager'].db, service_repository['database'])
        self.assertEqual(service_repository['manager'].mail, service_repository['mail'])

    def test_with_config_file_overriden(self):
        service_repository = repository.ServicesRepository()
        service_repository.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.ini'),
                                {'services': {'mail': {'host': 'smtp.local'}}})

        self.assertIsInstance(service_repository['mail'], services.Mail)
        self.assertEqual(service_repository['mail'].host, 'smtp.local')
        self.assertEqual(service_repository['mail'].port, 52)
        self.assertEqual(service_repository['mail'].timeout, 300.0)

        self.assertIsInstance(service_repository['database'], services.Database)
        self.assertEqual(service_repository['database'].host, "database.local")
        self.assertEqual(service_repository['database'].port, 5432)
        self.assertTrue(service_repository['database'].debug)

        self.assertIsInstance(service_repository['manager'], services.Manager)
        self.assertEqual(service_repository['manager'].db, service_repository['database'])
        self.assertEqual(service_repository['manager'].mail, service_repository['mail'])


class TestMissingServicesRepository(unittest.TestCase):
    def test_missing_service(self):
        service_repository = repository.MissingServicesRepository()

        with self.assertRaises(weedi.exc.ServiceMissing) as raised_ctx:
            service_repository.load()
        raised_exc = raised_ctx.exception
        self.assertEqual(str(raised_exc), 'mail')


class TestMissingConfigServicesRepository(unittest.TestCase):
    def test_missing_config_in_config_file(self):
        service_repository = repository.ConfigurationServicesRepository()
        with self.assertRaises(weedi.exc.WrongConfiguration) as raised_ctx:
            service_repository.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.ini'))
        raised_exc = raised_ctx.exception
        self.assertTrue('section "[services_configuration / config]", parameter "param1": False' in str(raised_exc))
        self.assertTrue('section "[services_configuration / config]", parameter "param2": False' in str(raised_exc))

    def test_missing_config_without_config_file(self):
        service_repository = repository.ConfigurationServicesRepository()
        with self.assertRaises(weedi.exc.WrongConfiguration) as raised_ctx:
            service_repository.load()
        raised_exc = raised_ctx.exception
        self.assertTrue('file "None", section "[services_configuration]", parameter "None": False' in str(raised_exc))


class TestUnpriorizedServicesRepository(unittest.TestCase):
    def test_wrong_priority_for_dependency(self):
        service_repository = repository.UnpriorizedServicesRepository()
        with self.assertRaises(weedi.exc.ServiceWrongPriority) as raised_ctx:
            service_repository.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.ini'))
        raised_exc = raised_ctx.exception
        self.assertEqual(str(raised_exc), 'database')


if __name__ == '__main__':
    unittest.main()
