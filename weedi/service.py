# -*- coding: utf-8 -*-

from . import loadable


class Service(loadable.Loadable):
    """ A special kind of service implementing a `start` and `stop` method.
    Useful to automatically start services on startup (for example tcpserver, ...)
    """

    def start(self):
        pass

    def stop(self):
        pass
