#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, The QiiTa Project"
__credits__ = ["Jose Antonio Navas Molina", "Joshua Shorenstein"]
__license__ = "BSD"
__version__ = "0.0.1-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.edu"
__status__ = "Development"

from qiita.core.exceptions import QiiTaSampleError

STATUS = ['proposed', 'private', 'public']


class QiiTaSample(object):
    """Models a sample of QiiTa"""

    def __init__(self, name, metadata, id=None):
        """"""
        pass