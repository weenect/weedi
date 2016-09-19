# Weedi

[![Build Status](https://travis-ci.org/weenect/weedi.svg?branch=master)](https://travis-ci.org/weenect/weedi)

## Introduction

Weedi is a dependency injection container based on [setuptools](https://setuptools.readthedocs.io/en/latest/) and [entry points](https://setuptools.readthedocs.io/en/latest/pkg_resources.html#entry-points).

It was first developed by [@Net-ng](https://github.com/Net-ng) and later opensourced and maintained by Weenect.

It is tested for python's versions 2.7, 3.3, 3.4 and 3.5

## Installation

You will need to have `setuptools` installed and to use it in your project as weedi uses the `entry_points` feature.

You can add `weedi` as a dependency of your project in your setup.py :

```python
from setuptools import setup, find_packages

setup(
    ...
    install_requires=('weedi'),
    ...
)
```

Then run `python setup.py install` or `python setup.py develop`

## Usage

Let's suppose you are managing locators and you have a service LocatorManager which depends on the database.

You will have these class in a module `services.py` :

``` python
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


class LocatorManager(loadable.Service):
    def __init__(self, database_service):
        self.db = database_service
```

You need to register these services in the `entry_points` or your project `setup.py`.

``` python
setup(
    ...
    entry_points='''
        [services]
        database = my_project.services:Database
        manager = my_project.services:LocatorManager
    '''
    ...
)
```

*Note : the name of the argument in LocatorManager constructor is database_service. This is the concatenation of the code of the database entry point and the string `_service`. This is the way the library recognizes that it needs to inject the database service when it instanciates the manager service.*

Then, you need to configure your container. Let's create a module `repository.py`. When creating a container, you need to define the name of the section managed by this repository in the entry points (here, it will be `services`) and the name of the section in the config file for this repository (cf config.ini below, it will be `services` too).

``` python
import weedi.loadables_repository as loadables_repository


class ServicesRepository(loadables_repository.LoadablesRepository):
    entry_point = 'services'
    conf_section = 'services'
```

The database service will have default value injected when it is created based on its spec. You can override this by creating a config file `config.ini` :

```ini
[services]

[[database]]
host = "database.local"
port = 5432
debug = True
```

Everything is ready. You just have to start your container.

```python
service_repository = ServicesRepository()
service_repository.load('path_to/config.ini')
```

You can access the services from the container :

```python
database_service = service_repository['database']
locator_manager_service = service_repository['manager']
```

You can inject these services in an object by constructor or by method :

```python
class ObjectNeedsService(object):
  def __init__(self, database_service):
    self.db = database_service
    self.manager = None

  def set_services(self, manager_service):
    self.manager = manager_service

new_instance = service_repository(ObjectNeedsService)
assert new_instance.db == service_repository['database']
assert new_instance.manager is None
service_repository(new_instance.set_services)
assert new_instance.db == service_repository['database']
assert new_instance.manager == service_repository['manager']
```

**The `project` folder is used to both run functional tests and to provide examples of use cases. Don't hesitate to go see the [test cases](https://github.com/weenect/weedi/blob/master/project/project/tests.py)**
