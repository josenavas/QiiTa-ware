from qiita_ware.connections import postgres
from psycopg2 import Error as PostgresError
from json import dumps


def get_postgres_cursor():
    """ Returns a Postgres cursor

    Inputs: None

    Returns:
        pgcursor: the postgres.cursor()

    Raises a RuntimeError if the cursor cannot be created
    """
    try:
        pgcursor = postgres.cursor()
    except PostgresError, e:
        raise RuntimeError("Cannot get postgres cursor! %s" % e)
    return pgcursor


def _check_sql_args(sql_args):
    """ Checks that sql_args have the correct type

    Inputs:
        sql_args: SQL arguments

    Raises a TypeError if sql_args does not have the correct type, otherwise
        it just returns the execution to the caller
    """
    # Check that sql arguments have the correct type
    if type(sql_args) is not tuple:
        raise TypeError("sql_args should be tuple. Found %s " % type(sql_args))


def sql_execute_fetchall(sql, sql_args):
    """ Executes a fetchall SQL query

    Inputs:
        sql: string with the SQL query
        sql_args: tuple with the arguments for the SQL query

    Returns:
        A boolean indicating if the query was successful
        The results of the fetchall query as a list of tuples
        A string with an error message, if the query failed
    """
    # Check that sql arguments have the correct type
    _check_sql_args(sql_args)
    # Get the cursor
    pgcursor = get_postgres_cursor()
    # Execute the query
    try:
        pgcursor.execute(sql, sql_args)
        result = pgcursor.fetchall()
        postgres.commit()
        pgcursor.close()
    except PostgresError, e:
        pgcursor.close()
        postgres.rollback()
        return False, None, "Error running SQL query"
    return True, result, ""


def sql_execute_fetchone(sql, sql_args):
    """ Executes a fetchone SQL query

    Inputs:
        sql: string with the SQL query
        sql_args: tuple with the arguments for the SQL query

    Returns:
        A boolean indicating if the query was successful
        The results of the fetchone query as a tuple
        A string with an error message, if the query failed
    """
    # Check that sql arguments have the correct type
    _check_sql_args(sql_args)
    # Get the cursor
    pgcursor = get_postgres_cursor()
    # Execute the query
    try:
        pgcursor.execute(sql, sql_args)
        result = pgcursor.fetchone()
        postgres.commit()
        pgcursor.close()
    except PostgresError, e:
        pgcursor.close()
        postgres.rollback()
        return False, None, "Error running SQL query"
    return True, result, ""


def sql_execute(sql, sql_args):
    """ Executes an SQL query with no results

    Inputs:
        sql: string with the SQL query
        sql_args: tuple with the arguments for the SQL query

    Returns:
        A boolean indicating if the query was successful
        A string with an error message, if the query failed
    """
    # Check that sql arguments have the correct type
    _check_sql_args(sql_args)
    # Get the cursor
    pgcursor = get_postgres_cursor()
    # Execute the query
    try:
        pgcursor.execute(sql, sql_args)
        postgres.commit()
        pgcursor.close()
    except PostgresError, e:
        pgcursor.close()
        postgres.rollback()
        return False, "Error running SQL query"
    return True, ""


def sql_executemany(sql, sql_args_list):
    """ Executes an executemany SQL query with no results

    Inputs:
        sql: string with the SQL query
        sql_args_list: list with tuples with the arguments for the SQL query

    Returns:
        A boolean indicating if the query was successful
        A string with an error message, if the query failed
    """
    # Check that sql arguments have the correct type
    for sql_args in sql_args_list:
        _check_sql_args(sql_args)
    # Get the cursor
    pgcursor = get_postgres_cursor()
    # Execute the query
    try:
        pgcursor.executemany(sql, sql_args_list)
        postgres.commit()
        pgcursor.close()
    except PostgresError, e:
        pgcursor.close()
        postgres.rollback()
        return False, "Error running SQL query"
    return True, ""

##############################
#  End of SQL aux functions  #
##############################


def get_completed_analyses_by_user(username):
    """ Given a user, retrieves its completed analyses

    Inputs:
        username: string with the QiiTa user name

    Returns:
        A boolean indicating if the data is available
        A list with all the analysis name of the current user
        A string with an error message, if the data is not available
    """
    # Build the SQL query
    SQL = """SELECT DISTINCT analysis_name FROM qiita_analysis
            WHERE qiita_username = %s AND analysis_done = true ORDER BY
            analysis_name"""
    # Execute the query
    success, result, err = sql_execute_fetchall(SQL, (username,))
    if success:
        if not result:
            # Username does not have any completed analysis
            return True, [], ""
        # Fetchall returns a list of tuples, get a list of strings
        result = [res[0] for res in result]
        return True, result, ""
    # Something went wrong with the query
    return False, None, "Error getting the analyses by user: %s" % err


def check_user_exists(username):
    """ Given a user, check if it exists

    Inputs:
        username: string with the QiiTa user name to check

    Returns:
        A boolean indicating if the data is available
        A boolean indicating if the user exists
        A string with an error message, if the data is not available
    """
    # Build the SQL query
    SQL = "SELECT count(1) FROM qiita_users WHERE qiita_username = %s"
    # Execute the query
    success, result, err = sql_execute_fetchone(SQL, (username,))
    if success:
        # Fetchone returns a tuple with a single integer that should be
        # 1 if the user exists and 0 if does not
        result = True if result[0] else False
        return True, result, ""
    # Something went wrong with the query
    return False, None, "Error checking user exists: %s" % err


def check_analysis_exists(username, analysis_name):
    """ Given a QiiTa analysis, check if it exists

    Inputs:
        username: string with the QiiTa user name
        analysis_name: name of the QiiTa analysis

    Returns:
        A boolean indicating if the data is available
        A boolean indicating if the analysis exists
        A string with an error message, if the data is not available
    """
    # Build the SQL query
    SQL = """SELECT count(1) FROM qiita_analysis
            WHERE qiita_username = %s AND analysis_name = %s"""
    # Execute the query
    success, result, err = sql_execute_fetchone(SQL, (username, analysis_name))
    if success:
        # Fetchone returns a tuple with a single integer that should be
        # 1 if the analysis exists and 0 if does not
        result = True if result[0] else False
        return True, result, ""
    # Something went wrong with the query
    return False, None, "Error checking %s exists: %s" % (analysis_name, err)


def add_user(username, password):
    """ Adds a new user to the system

    Inputs:
        username: the new QiiTa user name
        password: the password of the new user

    Returns:
        A boolean indicating if the user was added to the system
        A string with an error message, if the user was not added
    """
    # Build the SQL query
    SQL = """INSERT INTO qiita_users (qiita_username, qiita_password)
            VALUES (%s, %s)"""
    # Execute the query
    success, error = sql_execute(SQL, (username, password))
    # Build the error message if the user was not added
    error = "" if success else "Cannot add user %s: %s" % (username, error)
    return success, error


def check_credentials(username, password):
    """ Checks if password is correct for username

    Inputs:
        username: string with the QiiTa user name
        password: the password to check

    Returns:
        A boolean indicating if the data is available
        A boolean indicating if the password is correct
        A string with an error message, if the data is not available
    """
    # Build the SQL query
    SQL = """SELECT qiita_password from qiita_users WHERE
            qiita_username = %s"""
    # Execute the query
    success, result, err = sql_execute_fetchone(sql, (username, ))
    if success:
        if result is None:
            return False, None, "User does not exist"
        # Check if the password is correct
        return True, password == result[0], ""
    # Something went wrong with the query
    return False, None, "Error getting password for %s: %s" % (username,
                                                               err)


def get_analysis_status(username, analysis_name):
    """ Returns if the analysis is done or not

    Inputs:
        username: string with the QiiTa user name
        analysis_name: name of the QiiTa analysis

    Returns:
        A boolean indicating if the data is available
        A boolean indicating if the analysis is done
        A string with an error message, if the data is not available
    """
    # Build the SQL query
    SQL = """SELECT analysis_done FROM qiita_analysis WHERE
            qiita_username = %s AND analysis_name = %s"""
    # Execute the query
    success, result, err = sql_execute_fetchone(SQL, (username, analysis_name))
    if success:
        if result is None:
            # Raising an error because this should be a programming error
            raise ValueError("Analysis %s does not exists for user %s" %
                             (analysis_name, username))
        # Fetchone returns a tuple with a single value, get the boolean
        return True, bool(result[0]), ""
    # Something went wrong with the query
    return False, None, "Error getting %s status: %s" % (analysis_name, err)


def get_jobs_from_analysis(username, analysis_name):
    """ Returns the list of jobs of the given analysis

    Inputs:
        username: string with the QiiTa user name
        analysis_name: name of the QiiTa analysis

    Returns:
        A boolean indicating if the data is available
        A list with strings with job identifiers in datatype:job_function
            format
        A string with an error message, if the data is not available
    """
    # Build the SQL query
    SQL = """SELECT job_datatype, job_type FROM qiita_job
                WHERE qiita_username = %s AND analysis_name = %s"""
    # Execute the query
    success, result, err = sql_execute_fetchall(SQL, (username, analysis_name))
    if success:
        if result:
            # Fetchall returns a tuple with (datatype, job_function)
            # format to string
            job_list = ["%s:%s" % (j[0], j[1]) for j in result]
        else:
            # The are no jobs for the current analysis
            job_list = []
        return True, job_list, ""
    # Something went wrong with the query
    return False, None, "Error getting jobs from %s: %s" % (analysis_name, err)


def get_jobs_info_from_analysis(username, analysis_name):
    """ Returns the list of jobs objects for the given analysis

    Inputs:
        username: string with the QiiTa user name
        analysis_name: name of the QiiTa analysis

    Returns:
        A boolean indicating if the data is available
        A list with the job objects of the analysis
        A string with an error message, if the data is not available
    """
    # Build the SQL
    SQL = """SELECT * FROM qiita_job WHERE qiita_username = %s AND
            analysis_name = %s"""
    # Execute the query
    success, result, err = sql_execute_fetchall(SQL, (username, analysis_name))
    if success:
        if result is None:
            # Fetchall returns None if no matches
            # we should return an empty list
            job_list = []
        else:
            # TODO: Build the actual objects
            job_list = result
        return True, job_list, ""
    # Something went wrong with the query
    return False, None, "Error getting jobs from %s: %s" % (analysis_name, err)


def get_running_analyses_by_user(username):
    """ Returns a list of tuples with (analysis_name, timestamp) format

    Inputs:
        username: string with the QiiTa user name

    Returns:
        A boolean indicating if the data is available
        A list with the tuples
        A string with an error message, if the data is not available
    """
    # Build the SQL
    SQL = """SELECT analysis_name, analysis_timestamp FROM qiita_analysis
            WHERE qiita_username = %s AND analysis_done = false"""
    # Execute the query
    success, result, err = sql_execute_fetchall(SQL, (username,))
    if success:
        if result is None:
            # Fetchall returns None if no matches
            # we should return an empty list
            result = []
        return True, result, ""
    # Something went wrong with the query
    return False, None, ("Error retrieving running analyses for user %s: %s"
                         % (username, err))


def delete_analysis(username, analysis_name):
    """ Removes the given analysis from the system

    Inputs:
        username: string with the QiiTa user name
        analysis_name: name of the QiiTa analysis

    Raises a RuntimeError if the analysis can not be deleted, otherwise
        it just returns the execution to the caller
    """
    # NOTE remove results
    # First remove all the jobs related with the given analysis
    # Build the SQL
    SQL = """DELETE FROM qiita_job WHERE qiita_username = %s AND
        analysis_name = %s"""
    # Execute the query
    success, err = sql_execute(SQL, (username, analysis_name))

    if not success:
        # Raising an error because it's a runtime issue
        raise RuntimeError("Cannot delete jobs for analysis %s: %s" %
                           (analysis_name, err))

    # Now remove the actual analysis
    # Build the SQL
    SQL = """DELETE FROM qiita_analysis WHERE qiita_username = %s AND
        analysis_name = %s"""
    # Execute the query
    success, err = sql_execute(SQL, (username, analysis_name))

    if not success:
        # Raising an error because it's a runtime issue
        raise RuntimeError("Cannot delete analysis %s: %s" % (analysis_id,
                                                              err))


def set_job_done(job):
    """ Mark the given job as completed, adding results and/or the error

    Inputs:
        job: the job object

    Returns:
        A boolean indicating if the job was modified
        A string with an error message, if the job was not modified
    """
    # Create a tuple with the SQL values
    # Format: (SQL list of output files, error, datatype, job run, analysis id)
    raise NotImplementedError("TODO")
    sql_args = ("{%s}" % ','.join(results), error, datatype, job,
                analysis_id)
    # Update job in job table to done and with their results
    # Build the SQL
    SQL = """UPDATE qiita_job SET job_done = true, job_results = %s,
        job_error = %s WHERE job_datatype = %s AND job_type = %s AND
        analysis_id = %s"""
    # Execute the query
    success, err = sql_execute(SQL, sql_args)
    # Build the error message if not succeeded
    error_msg = "" if success else "Cannot set job done: %s" % err
    return success, error_msg


def check_all_jobs_done(username, analysis_name):
    """ Checks if all jobs for the given analysis are done

    Inputs:
        username: string with the QiiTa user name
        analysis_name: name of the QiiTa analysis

    Returns:
        A boolean indicating if the data is available
        A boolean indicating if all the jobs are done
        A string with an error message, if the data is not available
    """
    # Check that all the jobs from current analysis are done
    # Build the SQL
    SQL = """SELECT job_done FROM qiita_job WHERE
        qiita_username = %s AND analysis_name = %s"""
    # Execute the query
    success, result, err = sql_execute_fetchall(SQL, (analysis_id,))

    if success:
        if result is None:
            # The analysis does not exist -> programming error
            raise ValueError("Analysis %s does not exist!" % analysis_id)
        # Fetchall returns a list of tuples with a single element
        # of type bool. Check that all booleans are true
        return True, all([status[0] for status in result]), ""
    # Something went wrong with the query
    return False, None, ("Cannot check jobs status for analysis %s: %s" %
                         (analysis_name, err))


def set_analysis_done(username, analysis_name):
    """ Sets the given analysis as completed

    Inputs:
        username: string with the QiiTa user name
        analysis_name: name of the QiiTa analysis

    Returns:
        A boolean indicating if the analysis was modified
        A string with an error message, if the analysis was not modified
    """
    # Update analysis to done in analysis table
    # Build the SQL
    SQL = """UPDATE qiita_analysis SET analysis_done = true WHERE
        qiita_username = %s AND analysis_name = %s"""
    # Execute the query
    success, err = sql_execute(SQL, (username, analysis_name))
    # Build the error message if not succeeded
    error_msg = "" if success else "Cannot set analysis done: %s" % err
    return success, error_msg


def add_analysis(analysis_data):
    """ Adds a new analysis to the system

    Inputs:
        analysis_data: QiiTaAnalysis object

    Returns:
        A boolean indicating if the analysis was added
        A string with an error message, if the analysis was not added
    """
    # Insert analysis into the postgres analysis table
    raise NotImplementedError("TODO")
    SQL = """INSERT INTO qiita_analysis (qiita_username, analysis_name,
        analysis_studies, analysis_metadata, analysis_timestamp) VALUES
        (%s, %s, %s, %s, 'now')"""
    sql_studies_list = "{%s}" % ','.join(analysis_data.get_studies())
    sql_metadata_list = "{%s}" % ','.join(analysis_data.get_metadata())
    sql_args = (user, analysis_name, sql_studies_list, sql_metadata_list)
    success, err = sql_execute(SQL, sql_args)
    if not success:
        return False, "Can't create analysis: %s" % err

    # Insert all jobs into jobs table
    SQL = """INSERT INTO qiita_job (qiita_username, analysis_name,
        job_datatype, job_function, job_options) VALUES (%s, %s, %s, %s, %s)"""
    sql_args_list = []
    for datatype in analysis_data.get_datatypes():
        for job in analysis_data.get_jobs(datatype):
            sql_args_list.append((username, analysis_name, datatype, job,
                                  dumps(analysis_data.get_options(datatype,
                                                                  job))))

    success, error_msg = sql_executemany(SQL, sql_args_list)
    error_msg = "" if success else "Cannot set analysis done: %s" % error_msg
    return success, error_msg
