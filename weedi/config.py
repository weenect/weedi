# -*- coding: utf-8 -*-
#
# (c) 2016 Hareau SAS / Weenect, https://www.weenect.com
#
# This file is part of the weedi library
#
# MIT License : https://raw.githubusercontent.com/weenect/weedi/master/LICENSE.txt

"Helper to validate a configuration"

import configobj
from validate import Validator

import weedi.exc as exc


def _validate(filename, config):
    """Validate a :class:`configobj.ConfigObj` object

    :param str filename: the path to the configuration file
    :param config: the ``ConfigObj`` object, created from the configuration file
    :type config: :class:`configobj.ConfigObj`
    :return: yield the error messages
    :rtype: iterator or str
    """
    errors = configobj.flatten_errors(config, config.validate(Validator(), preserve_errors=True))

    for sections, name, error in errors:
        yield 'file "%s", section "[%s]", parameter "%s": %s' % (filename, ' / '.join(sections), name, error)


def validate(filename, config):
    """Validate a :class:`configobj.ConfigObj` object

    :param str filename: the path to the configuration file
    :param config: the ``ConfigObj`` object, created from the configuration file
    :type config: :class:`configobj.ConfigObj`
    :return: True if configuration valid else raise Exception
    :rtype: bool
    :raise: :class:`weedi.exc.WrongConfiguration` if invalid configuration
    """
    errors = list(_validate(filename, config))
    if errors:
        raise exc.WrongConfiguration('\n'.join(errors))

    return True
