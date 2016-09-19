# -*- coding: utf-8 -*-
#
# (c) 2016 Hareau SAS / Weenect, https://www.weenect.com
#
# This file is part of the weedi library
#
# MIT License : https://raw.githubusercontent.com/weenect/weedi/master/LICENSE.txt

"The repository of all services in charge of loading the configuration, instanciating the services and injecting them"

import logging
import inspect

import configobj
import pkg_resources

import weedi.config as config
import weedi.exc as exc


class LoadablesRepository(dict):
    """Base class of the service repository in charge of loading the service list, their configuration, instanciating
    them and injecting them in other services

    :param str conf_filename: the path to the configuration file
    :param conf: optionnal and additional configuration that will be merged with the one found in the configuration file
    :type conf: dict or :class:`configobj.ConfigObj`
    :param logger: A custom logger instance
    :type logger: :class:`logging.Logger`
    """

    entry_point = None
    "the name of the entry point managed by the repository"

    conf_section = None
    """the name of the configuration section in the file for the services managed by the repository.
    Most of the time it will have the same value as entry_point"""

    def __init__(self, conf_filename=None, conf={}, logger=None):
        self.logger = logger or logging.getLogger('weedi')

        if conf_filename is not None:
            self.load(conf_filename, conf)

    def load(self, conf_filename=None, conf={}):
        """Load the configuration from the config file, configure and instanciate the services and register them in
        the repository

        :param str conf_filename: the path to the configuration file
        :param conf: optionnal and additional configuration that will be merged with the one found in the configuration file
        :type conf: dict or :class:`configobj.ConfigObj`
        """
        self._discover()

        loadables_conf = self._read_config(conf_filename, conf)

        for name, loadable in sorted(self.items(), key=lambda item: item[1].load_priority):
            service_conf = loadables_conf.get(name, {})

            try:
                self.logger.debug("Loading %s <%s> with configuration %r", self.entry_point, name, service_conf)
                self.register(name, loadable, service_conf)
            except:
                self.logger.critical("%s <%s> can't be loaded with configuration %r", self.entry_point, name, service_conf)
                raise

    def _discover(self):
        """Load the service found inside this repository configured `entry_point`. After its execution, the repository
        will be a dict with keys as the service code and values as the service class"""
        self.update({entry.name: entry.load() for entry in pkg_resources.iter_entry_points(self.entry_point)})

    def _read_config(self, conf_filename, conf):
        """Read the configuration from the file and return the configuration section used by this repository

        :param str conf_filename: the path to the configuration file
        :param conf: optionnal and additional configuration that will be merged with the one found in the configuration file
        :type conf: dict or :class:`configobj.ConfigObj`
        :return: the configuration section of the ConfigObj used by this repository
        :rtype: :class:`configobj.Section`
        """
        if not self.conf_section:
            return dict(conf)

        spec = {name: loadable.spec for name, loadable in self.items()}
        spec = configobj.ConfigObj({self.conf_section: spec}, encoding='utf-8')

        loadables_conf = configobj.ConfigObj(conf_filename, configspec=spec, interpolation='Template', encoding='utf-8')
        loadables_conf.merge(conf)
        config.validate(conf_filename, loadables_conf)

        return loadables_conf[self.conf_section]

    def register(self, name, loadable, service_conf):
        """Instanciate and register a service inside the repository.

        .. note:: Can be overriden in child repository if needed.

        :param str name: the name/code of the service as configured in the entry_point
        :param class loadable: the class of the service as configured in the entry_point
        :param service_conf: the configuration needed by the service constructor to be instanciated
        :type service_conf: :class:`configobj.Section`
        """
        self[name] = self(loadable, **service_conf)

    def check_services_injection(self, f):
        """Inspect `f` to see if it is dependent from other services

        :param f: the class of the service to be instanciated or a function setter of an instanciated service
        :return: a dict of the services needed by `f` to be instanciated or invoked
        """
        args = inspect.getargspec(f.__init__ if isinstance(f, type) else f)

        services = dict(zip(reversed(args.args), reversed(args.defaults or ())))
        services.update({name + '_service': service for name, service in self.items() if not inspect.isclass(service)})
        services['services_service'] = self

        try:
            return {name: services[name] for name in args.args if name.endswith('_service')}
        except KeyError as e:
            name = e.args[0][:-8]
            if name not in self:
                self.logger.critical("Service %s <%s> doesn't exist", self.entry_point, name)
                raise exc.ServiceMissing(name)
            else:
                self.logger.critical("Service %s <%s> has not been priorized", self.entry_point, name)
                raise exc.ServiceWrongPriority(name)

    def __call__(self, f, *args, **kw):
        """ The injector method. It injects the service needed by `f`, calls it and returns it

        :param f: a callable object
        :type f: can be a class, a function or e mathod
        :return: the result of executing `f`
        """
        services = self.check_services_injection(f)
        services.update(kw)

        return f(*args, **services)
