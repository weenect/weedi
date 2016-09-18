import weedi.loadables_repository as loadables_repository


class ServicesRepository(loadables_repository.LoadablesRepository):
    entry_point = 'services'
    conf_section = 'services'


class MissingServicesRepository(loadables_repository.LoadablesRepository):
    entry_point = 'services.missing'
    conf_section = 'services'


class ConfigurationServicesRepository(loadables_repository.LoadablesRepository):
    entry_point = 'services.configuration'
    conf_section = 'services_configuration'


class UnpriorizedServicesRepository(loadables_repository.LoadablesRepository):
    entry_point = 'services.priority'
    conf_section = 'services'
