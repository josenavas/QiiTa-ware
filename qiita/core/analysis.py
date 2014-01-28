#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, The QiiTa Project"
__credits__ = ["Jose Antonio Navas Molina", "Joshua Shorenstein"]
__license__ = "BSD"
__version__ = "0.0.1-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.edu"
__status__ = "Development"

from qiita.core.exceptions import QiiTaAnalysisError

STATUS = ["construction", "running", "completed", "lock"]


class QiiTaAnalysis(object):
    """Models an analysis of QiiTa"""

    def __init__(self, name, a_id=None, samples=None,
                 metadata=None, jobs=None, status=None, pmid=None):
        """"""
        self._id = a_id
        self._name = name
        if samples and type(samples) is not list:
            raise QiiTaAnalysisError("samples should be a list")
        self._samples = samples if samples else []
        if metadata and type(metadata) is not list:
            raise QiiTaAnalysisError("metadata should be a list")
        self._metadata = metadata if metadata else []
        if jobs and type(jobs) is not list:
            raise QiiTaAnalysisError("jobs should be a list")
        self._jobs = jobs if jobs else []
        if status and status not in STATUS:
            raise QiiTaAnalysisError("Status not recognized %s" % status)
        self._status = status if status else "construction"
        self._pmid = pmid
        # Add timestamps

    def get_name(self):
        """"""
        return self._name

    def get_id(self):
        """"""
        return self._id

    def get_samples(self):
        """"""
        for sample in self._samples:
            yield sample

    def get_metadata(self):
        """"""
        for metadata in self._metadata:
            yield metadata

    def get_jobs(self):
        """"""
        for job in jobs:
            yield job

    def get_status(self):
        """"""
        return self._status

    def get_pmid(self):
        """"""
        return self._pmid

    def set_name(self, name):
        """"""
        if self._status == "lock":
            raise QiiTaAnalysisError("analysis can't be changed. It's locked")
        self._name = name

    def set_id(self, id):
        """"""
        raise QiiTaAnalysisError("The id of an object can't be changed")

    def set_status(self, status):
        """"""
        if self._status == "lock":
            raise QiiTaAnalysisError("analysis can't be changed. It's locked")
        if status not in STATUS:
            raise QiiTaAnalysisError("Status not recognized %s" % status)
        self._status = status

    def set_pmid(self):
        """"""
        self._pmid = pmid

    def add_sample(self, sample):
        """"""
        if self._status == "lock":
            raise QiiTaAnalysisError("analysis can't be changed. It's locked")
        self._samples.append(sample)

    def add_metadata(self, metadata):
        """"""
        if self._status == "lock":
            raise QiiTaAnalysisError("analysis can't be changed. It's locked")
        self._metadata.append(metadata)

    def add_job(self, job):
        """"""
        if self._status == "lock":
            raise QiiTaAnalysisError("analysis can't be changed. It's locked")
        self._jobs.append(job)

    def remove_sample(self, sample):
        """"""
        if self._status == "lock":
            raise QiiTaAnalysisError("analysis can't be changed. It's locked")
        try:
            self._samples.remove(sample)
        except ValueError, e:
            raise QiiTaAnalysisError("The analysis does not contain sample: "
                                     "%s" % sample.get_name())

    def remove_metadata(self, metadata):
        """"""
        if self._status == "lock":
            raise QiiTaAnalysisError("analysis can't be changed. It's locked")
        try:
            self._metadata.remove(metadata)
        except ValueError, e:
            raise QiiTaAnalysisError("The analysis does not contain metadata "
                                     "%s" % metadata)

    def remove_job(self, job):
        """"""
        if self._status == "lock":
            raise QiiTaAnalysisError("analysis can't be changed. It's locked")
        try:
            self._jobs.remove(job)
        except ValueError, e:
            raise QiiTaAnalysisError("The analysis does not contain job: %s"
                                     % job)
