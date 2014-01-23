#!/usr/bin/env python

__author__ = "Joshua Shorenstein"
__copyright__ = "Copyright 2013, The QiiTa-pet Project"
__credits__ = ["Joshua Shorenstein", "Jose Antonio Navas Molina"]
__license__ = "BSD"
__version__ = "0.2.0-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

from qiita.qiita_ware.connections import lview, postgres, r_server
from time import sleep
from json import dumps
from random import randint
from redis.exceptions import RedisError
from psycopg2 import Error as PostgresError
from IPython.parallel.error import IPythonError

##################################
#         Helper functions       #
##################################


def push_notification(user, analysis, job, msg, files=[], done=False):
    """Creates JSON and takes care of push notification

    INPUTS:
        user: username of user owner of the analysis
        analysis: name of the analysis
        job: job that submits the message
        msg: the actual message to be pushed
        files: list of paths to the job output
        done: true if the job completed successfully, false otherwise

    OUTPUT:
        tuple (boolean, str): the boolean indicates if the push was successful,
            and the str contains the error in case of a failed push.
    """
    # Construct the json object message
    jsoninfo = {
        'analysis': analysis,
        'job': job,
        'msg': msg,
        'results': files,
        'done': 1 if done else 0
    }
    jsoninfo = dumps(jsoninfo)

    # Send the message
    try:
        # Need the rpush and publish for leaving page and if race condition
        r_server.rpush(user + ":messages", jsoninfo)
        r_server.publish(user, jsoninfo)
    except RedisError, e:
        # Push failed, return False and an error message
        return False, "Can't push!\n%s\n%s" % (e, str(jsoninfo))

    # Push successful, return True without any error message
    return True, None


@lview.remote(block=False)
def job_handler(user, analysis_id, analysis_name, datatype, job, opts):
    """

    INPUTS:
        user: username of user owner of the analysis
        analysis_id: DB id of the analysis
        analysis_name: name of the analysis
        datatype: job's datatype
        job: name of the job to run
        opts: arguments of the job

    Raises a RuntimeError if there is any error connecting with the DB
    """
    # Dictionary that maps job name with the actual function that
    # executes the job
    # NOTE: this will go away
    job_functions_dict = {
        'Alpha_Diversity': alpha_diversity,
        'Beta_Diversity': beta_diversity,
        'Procrustes': procrustes
    }

    # Build job identifier for message handling
    datatype_job = '%s:%s' % (datatype, job)
    # Push the job has been started
    push_notification(user, analysis_name, datatype_job, 'Running')

    # Run the actual job
    # NOTE: This is needed due to the dummy functions
    # we will need to remove this once we are calling
    # the real functions
    opts['datatype'] = datatype
    success, results = job_functions_dict[job](opts)
    if success:
        # Push the job finished successfully
        push_notification(user, analysis_name, datatype_job, 'Completed',
                          results, done=True)
        error = False
    else:
        # Push the job failed
        push_notification(user, analysis_name, datatype_job, 'ERROR',
                          done=True)
        results = []
        error = True

    # Mark current job as DONE
    success, error_msg = set_job_done(analysis_id, datatype, job, results,
                                      error)

    if not success:
        raise RuntimeError("Can't set job to done: %s" % error_msg)

    # Check if the other jobs of the same analysis are done
    success, result = check_all_jobs_done(analysis_id)

    if not success:
        raise RuntimeError("Can't check analysis with id %s status: %s" %
                           (analysis_id, result))

    if result:
        finish_analysis(user, analysis_id, analysis_name)


def finish_analysis(user, analysis_id, analysis_name):
    """Marks current analysis as done in the DB

    INPUTS:
        user: username of user owner of the analysis
        analysis_id: DB id of the analysis
        analysis_name: name of the analysis

    Raises a RuntimeError if there is any error connecting with the DB
    """
    success, error_msg = set_analysis_done(analysis_id)

    if success:
        # Wipe out all messages from redis list so no longer pushed to user
        for message in r_server.lrange(user + ':messages', 0, -1):
            if analysis_name in str(message):
                r_server.lrem(user + ':messages', message)

        # Finally, push finished state
        push_notification(user, analysis_name, 'done', 'allcomplete')
    else:
        raise RuntimeError("Can't set analysis %s to done: %s" % (analysis_id,
                                                                  error_msg))


def switchboard(user, analysis_data):
    """Fires off all jobs for a given analysis.

    INPUTS:
        user: username of user requesting job
        analysis_data: MetaAnalysisData object with all information in it.

    Raises a RuntimeError if there is any error connecting with the DB
    """
    analysis_name = analysis_data.get_analysis()

    success, result = add_analysis(analysis_data)

    if not success:
        return False, "Can't create analysis %s: %s" % (analysis_name, result)

    # Submit the jobs
    for datatype in analysis_data.get_datatypes():
        for job in analysis_data.get_jobs(datatype):
            opts = analysis_data.get_options(datatype, job)
            try:
                job_handler(user, analysis_id, analysis_name, datatype, job,
                            opts)
            except IPythonError, e:
                # Set job failed
                success, error_msg = set_job_done(analysis_id, datatype, job,
                                                  [], True)
                if not success:
                    raise RuntimeError("Can't set job to error: %s" %
                                       error_msg)
                # Push the job failed
                push_notification(user, analysis_name, datatype_job, 'ERROR',
                                  done=True)


###################################
#       Analysis functions        #
#       ------------------        #
# These dummy functions will be   #
# removed once we can call the    #
# real QIIME functions            #
###################################


def alpha_diversity(opts):
    """Dummy function"""
    sleep(randint(5, 10))
    datatype = opts['datatype']
    results = ["results/demo/alpha/%s/alpha_rarefaction_plots/rarefaction_plots.html" % datatype.lower()]
    return True, results


def beta_diversity(opts):
    """Dummy function"""
    sleep(randint(10, 20))
    datatype = opts['datatype']
    if datatype == "16S":
        results = ["results/demo/beta/emperor/unweighted_unifrac_16s/index.html",
                   "results/demo/beta/emperor/weighted_unifrac_16s/index.html"]
    else:
        results = ["results/demo/beta/emperor/%s/index.html" % datatype.lower()]
    return True, results


def procrustes(opts):
    """Dummy function"""
    # Push the job has been started
    sleep(randint(20, 20))
    results = ["results/demo/combined/plots/index.html"]
    return True, results
