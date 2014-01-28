#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, The QiiTa Project"
__credits__ = ["Jose Antonio Navas Molina", "Joshua Shorenstein"]
__license__ = "BSD"
__version__ = "0.0.1-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.edu"
__status__ = "Development"


class BaseStorageAPI(object):
    """Base class for the Storage API objects for the QiiTa-db backends"""

    def __init__(self):
        """Initializes the object"""
        pass

    def insert(self, object):
        """Inserts the object in the backend storage"""
        raise NotImplementedError("BaseStorageAPI.insert not implemented")

    def update(self, object):
        """Updates the object attributes in the backend storage"""
        raise NotImplementedError("BaseStorageAPI.update not implemented")

    def delete(self, id):
        """Deletes the object with id=id from the backend storage"""
        raise NotImplementedError("BaseStorageAPI.delete not implemented")

    def get(self, id):
        """Retrieves the object with id=id from the backend storage"""
        raise NotImplementedError("BaseStorageAPI.id not implemented")

    def search(self, searchObject):
        """Retrieves all the objects that match searchObject queries"""
        raise NotImplementedError("BaseStorageAPI.search not implemented")
