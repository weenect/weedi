import logging

import configobj
import pkg_resources

from . import config


logger = logging.getLogger('weedi')


class LoadablesRepository(dict):
    entry_point = None
    conf_section = None

    def __init__(self, conf_filename=None, conf=None, error=None):
        if conf is not None:
            self.load(conf_filename, conf, error)

    def read_config(self, conf_filename, conf, error):
        if not self.conf_section:
            return {}

        spec = {name: loadable.spec for name, loadable in self.items()}
        spec = configobj.ConfigObj({self.conf_section: spec}, encoding='utf-8')

        loadables_conf = configobj.ConfigObj(conf_filename, configspec=spec, interpolation='Template', encoding='utf-8')
        loadables_conf.merge(conf)
        config.validate(conf_filename, loadables_conf, error)

        return loadables_conf[self.conf_section]

    def register(self, name, loadable, service_conf):
        """
        Register a service.

        Override if needed.
        """
        self[name] = self(loadable, **service_conf)

    def load(self, conf_filename, conf, error):
        self._discover()

        loadables_conf = self.read_config(conf_filename, conf, error)

        for name, loadable in sorted(self.items(), key=lambda item: item[1].load_priority):
            service_conf = loadables_conf.get(name, {})

            try:
                logger.debug("Loading %s <%s> with configuration %r", self.entry_point, name, service_conf)
                self.register(name, loadable, service_conf)
            except:
                logger.critical("%s <%s> can't be loaded", self.entry_point.capitalize(), name)
                raise

    def _discover(self):
        self.update({entry.name: entry.load() for entry in pkg_resources.iter_entry_points(self.entry_point)})
