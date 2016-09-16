import weedi.services_repository as services_repository


class ServicesRepository(services_repository.BaseServicesRepository):
    entry_point = 'services'
    conf_section = 'services'
