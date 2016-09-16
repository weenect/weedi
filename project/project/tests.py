import os
import project.repository as repository

service_repository = repository.ServicesRepository()
service_repository.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.ini'), {}, None)
