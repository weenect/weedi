# -*- coding: utf-8 -*-

"Exceptions raised by the library"


class WeediException(Exception):
    "Base exception for all the one raised by the library"
    pass


class ServiceMissing(WeediException):
    "Raised when a service could not be found when instanciating another one"
    pass


class ServiceWrongPriority(WeediException):
    "Raised when trying to inject a service which has not been loaded yet"
    pass


class WrongConfiguration(WeediException):
    "Raised when there is an error in the configuration file"
    pass
