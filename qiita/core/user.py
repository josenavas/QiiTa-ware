#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, The QiiTa Project"
__credits__ = ["Jose Antonio Navas Molina", "Joshua Shorenstein"]
__license__ = "BSD"
__version__ = "0.0.1-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.edu"
__status__ = "Development"

from qiita.core.exceptions import QiiTaUserError


class QiiTaUser(object):
    """Models an user of QiiTa"""

    def __init__(self, username, password, email, level, address=None
                 lab=None, phone=None):
        """Initializes the QiiTaUser object"""
        self._id = username
        self._password = password
        self._email = email
        self._level = level
        self._address = address
        self._lab = lab
        self._phone = phone
        self._analyses = None
        self._studies = None
        self._shared_analyses = None
        self._shared_studies = None

    def check_password(self, check_pwd):
        """Checks that check_pwd is the user's password"""
        return self._password == check_pwd

    def get_username(self):
        """Retrieves the username"""
        return self._id

    def get_password(self):
        """Retrieves the user password"""
        raise QiiTaUserError("You are not supposed to see the password")

    def get_email(self):
        """Retrieves the user email"""
        return self._email

    def get_level(self):
        """Retrieves the user level"""
        return self._level

    def get_address(self):
        """Retrieves the user address"""
        return self._address

    def get_lab(self):
        """Retrieves the user lab"""
        return self._lab

    def get_phone(self):
        """Retrieves the user phone"""
        return self._phone

    def add_analysis(self, analysis):
        """Adds an analysis to the user list

        Inputs:
            analysis: QiiTaAnalysis object
        """
        self._analyses.append(analysis)

    def add_shared_analysis(self, analysis):
        """Adds a shared analysis to the user list

        Inputs:
            analysis: QiiTaAnalysis object
        """
        self._shared_analyses.append(analysis)

    def add_study(self, study):
        """Adds a study to the user list

        Inputs:
            study: QiiTaStudy object
        """
        self._studies.append(study)

    def add_shared_study(self, study):
        """Adds a shared study to the user list

        Inputs:
            study: QiiTaStudy object
        """
        self._shared_studies.append(study)

    def set_username(self, username):
        """Sets the username of the user

        Should never be changed - raises a QiiTaUserError always
        """
        raise QiiTaUserError("The username cannot be changed")

    def set_password(self, password):
        """Sets the password of the user"""
        self._password = password

    def set_email(self, email):
        """Sets the email of the user"""
        self._email = email

    def set_level(self, level):
        """Sets the level of the user"""
        self._level = level

    def set_address(self, address):
        """Sets the address of the user"""
        self._address = address

    def set_lab(self, lab):
        """Sets the lab of the user"""
        self._lab = lab

    def set_phone(self, phone):
        """Sets the phone of the user"""
        self._phone = phone

    def remove_analysis(self, analysis):
        """Removes the given analysis from the user list

        Inputs:
            analysis: QiiTaAnalysis object
        """
        self._analyses.remove(analysis)

    def remove_shared_analysis(self, analysis):
        """Removes the given analysis from the user shared list

        Inputs:
            analysis: QiiTaAnalysis object
        """
        self._shared_analyses.remove(analysis)

    def remove_study(self, study):
        """Removes the given study from the user list

        Inputs:
            study: QiiTaStudy object
        """
        self._studies.remove(study)

    def remove_shared_study(self, study):
        """Removes the given study from the user shared list

        Inputs:
            study: QiiTaStudy object
        """
        self._shared_studies.remove(study)
