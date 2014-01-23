#!/usr/bin/env python

__author__ = "Joshua Shorenstein"
__copyright__ = "Copyright 2013, The QiiTa Project"
__credits__ = ["Jose Antonio Navas Molina"]
__license__ = "BSD"
__version__ = "0.2.0-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"


class QiiTaAnalysis(object):
    """"""
    def __init__(self, user, name, studies=None, metadata=None, timestamp=None,
                 jobs=None, done=False):
        # The QiiTa user name of the owner of this QiiTa analysis
        self.user = user
        # The name of the QiiTa analysis, defined by the user
        self.name = name
        # List of studies involved in this QiiTa analysis
        self.studies = []
        # List of the metadata used in this QiiTa analysis
        self.metadata = []
        # The timestamp of this QiiTa analysis - ASK JOSH: starting time?
        self.timestamp = ""
        # List of QiiTa jobs that builds up this QiiTa analysis
        self.jobs = []
        # Holds if the analysis have been completed or not
        self.done = False

    def __str__(self):
        raise NotImplementedError("Jose, you forgot something!")

    def get_user(self):
        """"""
        return self.user

    def get_name(self):
        """"""
        return self.name

    def get_studies(self):
        """"""
        return self.studies

    def get_metadata(self):
        """"""
        return self.metadata

    def get_timestamp(self):
        """"""
        return self.timestamp

    def get_jobs(self):
        """"""
        return self.jobs

    def is_done(self):
        """"""
        return self.done