# -*- coding: utf-8 -*-

class Loadable(object):
    "Base class that all injectable services should extends"

    load_priority = 0
    "Priorize the loading of the service in case other later service are dependant"

    spec = {}
    "Dict to configure the constructor parameters of the service"

    def __init__(self):
        super(Loadable, self).__init__()
