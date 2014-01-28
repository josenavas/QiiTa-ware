#!/usr/bin/env python

__author__ = "Jose Antonio Navas Molina"
__copyright__ = "Copyright 2013, The QiiTa Project"
__credits__ = ["Jose Antonio Navas Molina", "Joshua Shorenstein"]
__license__ = "BSD"
__version__ = "0.0.1-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.edu"
__status__ = "Development"


def create_analysis(analysis_name, **kwargs):
    """ Adds a new QiiTa analysis to the system

    Inputs:
        analysis_name: the name of the new analysis
        kwargs: extra analysis information

    Returns:
        The new QiiTaAnalysis object

    Checks:
        - Valid analysis_name

    Raises an error if something went wrong
    """
    raise NotImplementedError("qiita_ware.api.analysis_manager: "
                              "create_analysis")


def update_analysis(analysis):
    """ Updates the analysis information in the system

    Inputs:
        analysis: a QiiTaAnalysis object

    Checks:
        - Analysis is mutable - double checked, should be embedded on the
            QiiTaAnalysis object

    Does not perform any data content check - assumed to be included on the
        QiiTaAnalysis obj
    Raises an error if something went wrong
    """
    raise NotImplementedError("qiita_ware.api.analysis_manager: "
                              "update_analysis")


def delete_analysis(analysis_id):
    """ Deletes the QiiTaAnalysis analysis_id from the system

    Inputs:
        analysis_id: the analysis id to remove

    Checks:
        - analysis exists
        - analysis status:
            Public: raise error
            Shared: if Force remove else error
            Private: remove
    """
    raise NotImplementedError("qiita_ware.api.analysis_manager: "
                              "delete_analysis")


def get_analysis(analysis_id):
    """ Retrieves the analysis_id object

    Inputs:
        analysis_id: the id of the analysis to retrieve

    Returns:
        The QiiTaAnalysis object

    Raises an error if something went wrong
    """
    raise NotImplementedError("qiita_ware.api.analysis_manager: get_analysis")


def search_analyses(analysis_name_hint, **kwargs):
    """ Retrieves all the analyses in the system that match the search query

    Inputs:
        user_id: the user that makes the search
        analysis_name_hint: string with a partial analysis name
        **kwargs: extra analysis information

    Returns:
        A list with all the QiiTaAnalysis objects that match the search query
            that are visible by the user_id
    """
    raise NotImplementedError("qiita_ware.api.analysis_manager: "
                              "search_analyses")


def stop_analysis(analysis_id):
    """ Stops all the running jobs of analysis_id

    Inputs:
        analysis_id: the analysis to be stopped
    """
    raise NotImplementedError("qiita_ware.api.analysis_manager: stop_analysis")


def publish_analysis(analysis_id):
    """ Makes analysis_id public

    Inputs:
        analysis_id: id of the analysis
    """
    raise NotImplementedError("qiita_ware.api.analysis_manager: "
                              "publish_analysis")

##############################################
#                                            #
# Functions only need in local installations #
#                                            #
##############################################


def submit_analysis_to_QiiTaMain(analysis_id, **kwargs):
    """ Submits anlysis_id to the QiiTa Main repository hosted in the
            Knight Lab

        Inputs:
            analysis_id: the analysis to upload
            kwargs: TBD
    """
    raise NotImplementedError("qiita_ware.api.analysis_manager: "
                              "submit_analysis_to_QiiTaMain")

############################################
#                                          #
# Functions only need if using QiiTa-pet   #
# as a front-end. Otherwise, there is no   #
# notion of users.                         #
#                                          #
############################################


def get_all_visible_analyses(user_id):
    """ Retrieves all the analysis visible by user_id

    Inputs:
        user_id: the user id

    Returns:
        A list with all QiiTaAnalysis objs that are visible by user_id
    """
    raise NotImplementedError("qiita_ware.api.analysis_manager: "
                              "get_all_visible_analyses")


def get_running_analyses(user_id):
    """ Retrieves all the running analysis visible by user_id

    Inputs:
        user_id: the user id

    Returns:
        A list with all QiiTaAnalysis objs that are running and visible
            by user_id
    """
    raise NotImplementedError("qiita_ware.api.analysis_manager: "
                              "get_running_analyses")


def get_completed_analyses(user_id):
    """ Retrieves all the completed analysis visible by user_id

    Inputs:
        user_id: the user id

    Returns:
        A list with all QiiTaAnalysis objs that are completed and visible
            by user_id
    """
    raise NotImplementedError("qiita_ware.api.analysis_manager: "
                              "get_completed_analyses")


def share_analysis(analysis_id, user_id):
    """ Shares the analysis_id with user_id

    Inputs:
        analysis_id: id of the analysis
        user_id: user to share the analysis with
    """
    raise NotImplementedError("qiita_ware.api.analysis_manager: "
                              "share_analysis")


def transfer_analysis(analysis_id, user_id):
    """ Transfers ownership of analysis_id to user_id

    Inputs:
        analysis_id: id of the analysis
        user_id: user to transfer ownership of the analysis to
    """
    raise NotImplementedError("qiita_ware.api.analysis_manager: "
                              "trasnfer_analysis")
