import weedi.loadable as loadable


class Database(loadable.Service):
    spec = {
        'host': 'string(default="localhost")',
        'port': 'integer(default=3306)',
        'debug': 'boolean(default=False)',
    }

    load_priority = -10

    def __init__(self, host, port, debug):
        self.host = host
        self.port = port
        self.debug = debug


class Mail(loadable.Service):
    spec = {
        'host': 'string(default="127.0.0.1")',
        'port': 'integer(default=25)',
        'timeout': 'float(default=120.0)'
    }

    load_priority = -10

    def __init__(self, host, port, timeout):
        self.host = host
        self.port = port
        self.timeout = timeout


class Manager(loadable.Service):
    def __init__(self, mail_service, database_service):
        self.mail = mail_service
        self.db = database_service


class ConfigurationNeededService(loadable.Service):
    spec = {
        'param1': 'string()',
        'param2': 'string()'
    }

    load_priority = -10

    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2


class DatabaseUnpriorized(Database):
    load_priority = 10
