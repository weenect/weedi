# -*- coding: utf-8 -*-

import inspect
import logging

from . import loadables_repository

logger = logging.getLogger('weedi')


class ServiceMissing(Exception):
    pass


class BaseServicesRepository(loadables_repository.LoadablesRepository):
    def check_services_injection(self, f):
        args = inspect.getargspec(f.__init__ if isinstance(f, type) else f)

        services = dict(zip(reversed(args.args), reversed(args.defaults or ())))
        services.update({name + '_service': service for name, service in self.items()})
        services['services_service'] = self

        try:
            return {name: services[name] for name in args.args if name.endswith('_service')}
        except KeyError as e:
            logger.critical("Service <%s> doesn't exist", e.args[0][:-8])
            raise ServiceMissing(e.args[0][:-8])

    def __call__(self, f, *args, **kw):
        services = self.check_services_injection(f)
        services.update(kw)

        return f(*args, **services)
