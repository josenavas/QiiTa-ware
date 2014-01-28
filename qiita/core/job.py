#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, The QiiTa Project"
__credits__ = ["Jose Antonio Navas Molina", "Joshua Shorenstein"]
__license__ = "BSD"
__version__ = "0.0.1-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.edu"
__status__ = "Development"

from qiita.core.exceptions import QiiTaJobError
from qiita.core.qiita_settings import DATATYPES, FUNCTIONS

STATUS = ["construction", "running", "completed", "internal_error",
          "user_error"]


class QiiTaJob(object):
    """Models a job of QiiTa"""

    def __init__(self, datatype, function, j_id=None, options=None,
                 results=None, status=None, error_msg=None):
        """"""
        self._id = j_id
        if datatype not in DATATYPES:
            raise QiiTaJobError("datatype not recognized: %s" % datatype)
        self.datatype = datatype
        # Maybe options are going to be included on function (pyqi)
        # TODO sanitize options
        if function not in FUNCTIONS:
            raise QiiTaJobError("function not recognized: %s" % function)
        # They might be object - default to a empty dict for lazyness
        self._options = options if options else {}
        self._results = results if results else []
        self._status = status if status else "construction"
        self._error_msg = error_msg

    # define get and set, and add/remove for results and update option
    # check status before setting
    # define __eq__ __neq__
