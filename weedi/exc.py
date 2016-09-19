# -*- coding: utf-8 -*-
#
# (c) 2016 Hareau SAS / Weenect, https://www.weenect.com
#
# This file is part of the weedi library
#
# MIT License : https://raw.githubusercontent.com/weenect/weedi/master/LICENSE.txt

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
