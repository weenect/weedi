# -*- coding: utf-8 -*-
#
# (c) 2016 Hareau SAS / Weenect, https://www.weenect.com
#
# This file is part of the weedi library
#
# MIT License : https://raw.githubusercontent.com/weenect/weedi/master/LICENSE.txt

"Provide parent class that services need to extend in order to be injectable"


class Loadable(object):
    "Base class that all injectable services should extends"

    load_priority = 0
    "Priorize the loading of the service in case other later service are dependant. (sorted by load_priority ascending)"

    spec = {}
    "Dict to configure the constructor parameters of the service"

    def __init__(self):
        super(Loadable, self).__init__()


class Service(Loadable):
    """A special kind of loadable implementing a `start` and `stop` method. Useful to automatically start services on
    startup (for example tcpserver, ...)
    """

    def start(self):
        pass

    def stop(self):
        pass
