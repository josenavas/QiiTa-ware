#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, The QiiTa Project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "BSD"
__version__ = "0.0.1-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.edu"
__status__ = "Development"

from qiita.core.exceptions import QiiTaError


class QiiTaWareError(QiiTaError):
    """Base clase for all QiiTa-ware exceptions"""
    pass


class UserNotExistsError(QiiTaWareError):
    """"""
    pass


class AnalysisNotExistsError(QiiTaWareError):
    """"""
    pass


class JobNotExistsError(QiiTaWareError):
    """"""
    pass


class StudyNotExistsError(QiiTaWareError):
    """"""
    pass
