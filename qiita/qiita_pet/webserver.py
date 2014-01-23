#!/usr/bin/env python

__author__ = "Joshua Shorenstein"
__copyright__ = "Copyright 2013, The QiiTa-pet Project"
__credits__ = ["Joshua Shorenstein", "Antonio Gonzalez",
               "Jose Antonio Navas Molina"]
__license__ = "BSD"
__version__ = "0.2.0-dev"
__maintainer__ = "Jose Antonio Navas Molina"
__email__ = "josenavasmolina@gmail.com"
__status__ = "Development"

#login code modified from https://gist.github.com/guillaumevincent/4771570

import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
from tornado.options import define, options
from os.path import dirname, join
import base64
import uuid
from hashlib import sha512

from qiita.qiita_pet.settings import SINGLE, COMBINED
from qiita.qiita_pet.message_handler import MessageHandler
from qiita.qiita_pet.meta_analysis import MetaAnalysisData
from qiita.qiita_ware.switchboard import switchboard

define("port", default=8888, help="run on the given port", type=int)

metaAnalysis = MetaAnalysisData()


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        """Overrides default method of returning user curently connected"""
        user = self.get_secure_cookie("user")
        if user is None:
            self.clear_cookie("user")
            return ''
        else:
            return user.strip('" ')

    def write_error(self, status_code, **kwargs):
        """Overrides the error page created by Tornado"""
        # Tornado forces to have this import here
        from traceback import format_exception
        if self.settings.get("debug") and "exc_info" in kwargs:
            exc_info = kwargs["exc_info"]
            # Get the HTML string with the traceback
            trace_list["%s<br />" % l for l in format_exception(*exc_info)]
            trace_info = ''.join(trace_list)
            # Get the HTML string with the request information
            request_list = ["<strong>%s</strong>: %s<br />" %
                            (k, self.request.__dict__[k]) for k in
                            self.request.__dict__.keys()]
            request_info = ''.join(request_list)
            # Get the generated error message
            error = exc_info[1]
            # Display the error page
            self.render('error.html', error=error, trace_info=trace_info,
                        request_info=request_info,
                        user=self.get_current_user())


class MainHandler(BaseHandler):
    """Index page"""
    @tornado.web.authenticated
    def get(self):
        username = self.get_current_user()
        # Get a list with the analyses of current user
        sucess, result, err = get_completed_analyses_by_user(username)
        # Check if we get the results
        if success:
            # Yes! Display them
            self.render("index.html", user=username, analyses=result, error="")
        else:
            # No! Display an error in the page
            self.render("index.html", user=username, analyses=[], error=err)


class AuthCreateHandler(BaseHandler):
    """User Creation page"""
    def get(self):
        try:
            error_message = self.get_argument("error")
        # Tornado can raise an Exception directly, not a defined type
        except Exception, e:
            error_message = str(e)

        self.render("create.html", user=self.get_current_user(),
                    errormessage=error_message)

    def post(self):
        username = self.get_argument("username", "")
        passwd = sha512(self.get_argument("password", "")).hexdigest()
        created, error = self.create_user(username, passwd)
        # Check if the user was created correctly
        if created:
            # Yes! Redirect him to the login page
            self.redirect(u"/auth/login/?error=User+created")
        else:
            # No! Keep in current page showing a message explaining the error
            error_msg = u"?error=" + tornado.escape.url_escape(error)
            self.redirect(u"/auth/create/" + error_msg)

    def create_user(self, username, password):
        """Creates a new user in the system

        Inputs:
            username: string with the new QiiTa username
            password: user password
        """
        # Sanity checks: neither the user name or password are empty strings
        if username == "":
            return False, "No username given!"
        if password == sha512("").hexdigest():
            return False, "No password given!"

        # Check to make sure user does not already exist
        success, result = check_user_exists(username)
        if not success:
            return False, result
        if result:
            return False, "Username already exists!"

        return add_user(username, password)


class AuthLoginHandler(BaseHandler):
    '''Login Page'''
    def get(self):
        try:
            error_message = self.get_argument("error")
        # Tornado can raise an Exception directly, not a defined type
        except Exception, e:
            error_message = ""

        self.render("login.html", user=self.get_current_user(),
                    errormessage=error_message)

    def check_login(self, username, password):
        success, result = check_credentials(username, password)
        if success:
            if result:
                return True, ""
            return False, "Login incorrect"
        return False, result

    def post(self):
        username = self.get_argument("username", "")
        passwd = sha512(self.get_argument("password", "")).hexdigest()
        auth, msg = self.check_login(username, passwd)
        if auth:
            self.set_current_user(username)
            self.redirect(self.get_argument("next", u"/"))
        else:
            error_msg = u"?error=%s" % \
                tornado.escape.url_escape(msg)
            self.redirect(u"/auth/login/" + error_msg)

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")


class AuthLogoutHandler(BaseHandler):
    '''Logout handler, no page necessary'''
    def get(self):
        self.clear_cookie("user")
        self.redirect("/")


class WaitingHandler(BaseHandler):
    '''Waiting Page'''
    @tornado.web.authenticated
    def get(self, analysis_name):
        username = self.get_current_user()

        success, result = get_analysis_status(username, analysis_name)
        if not success:
            self.render("waiting.html", user=username, analysis=analysis_name,
                        jobs=[], error=result)
            return
        # GET COMMENTED
        if result:
            self.redirect('/completed/%s' % analysis_name)
        else:
            success, result = get_jobs_from_analysis(username, analysis_name)
            if success:
                self.render("waiting.html", user=username,
                            analysis=analysis_name, jobs=result, error="")
            else:
                self.render("waiting.html", user=username,
                            analysis=analysis_name, jobs=[], error=result)

    @tornado.web.authenticated
    #This post function takes care of actual job submission
    def post(self, page):
        username = self.get_current_user()
        jobs = metaAnalysis.get_all_jobs()
        self.render("waiting.html", user=username,
                    analysis=metaAnalysis.get_analysis(), jobs=jobs,
                    error="")
        # Must call IPython after page call!
        switchboard(username, metaAnalysis)


class RunningHandler(BaseHandler):
    '''Currently running jobs list handler'''
    @tornado.web.authenticated
    def get(self):
        username = self.get_current_user()
        success, result = get_running_analyses_by_user(username)
        if success:
            self.render("runningmeta.html", user=username, analyses=result,
                        error="")
        else:
            self.render("runningmeta.html", user=username, analyses=[],
                        error=result)


class ShowJobHandler(BaseHandler):
    '''Completed job page'''
    @tornado.web.authenticated
    def get(self, analysis_name):
        user = self.get_current_user()
        self._render(username, analysis_name)

    @tornado.web.authenticated
    def post(self, page):
        analysis_name = self.get_argument('analysis')
        user = self.get_current_user()
        self._render(username, analysis_name)

    def _render(self, username, analysis_name):
        """"""
        success, result = get_jobs_info_from_analysis(username, analysis_name)
        if success:
            self.render("analysisinfo.html", user=user, analysis=analysis_name,
                        analysisinfo=result, error="")
        else:
            self.render("analysisinfo.html", user=user, analysis=analysis_name,
                        analysisinfo=[], error=result)


class DeleteAnalysisHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        user = self.get_current_user()
        analysis_name = self.get_argument('analysis')
        success, error_msg = delete_analysis(user, analysis_name)
        if success:
            self.redirect('/')
        else:
            raise RuntimeError("Cannot delete analysis %s: %s" %
                              (analysis_name, error_msg))


#ANALYSES and COMBINED lists are set in settings.py
class MetaAnalysisHandler(BaseHandler):
    def prepare(self):
        self.user = self.get_current_user()

    @tornado.web.authenticated
    def get(self, page):
        if page != '1':
            self.write('YOU SHOULD NOT ACCESS THIS PAGE DIRECTLY<br \>')
            self.write("You requested form page " + page + '<br \>')
            self.write('<a href="/">Home</a>')
        else:
            #global variable that is wiped when you start a new analysis
            metaAnalysis = MetaAnalysisData()
            metaAnalysis.set_user(self.user)
            self.render('meta1.html', user=self.user, error="")

    @tornado.web.authenticated
    def post(self, page):
        if page == '1':
            pass
        elif page == '2':
            analysis_name = self.get_argument('analysisname')
            # Check if metaAnalysis name already exists
            success, result = check_analysis_exists(self.user, analysis_name)
            if not success:
                raise RuntimeError("Name can't be checked: %s" % result)
            if result:
                self.render('meta1.html', user=self.user,
                            error="Analyis name already exists!")
                return

            metaAnalysis.set_analysis(analysis_name)
            metaAnalysis.set_studies(self.get_arguments('studiesView'))

            if metaAnalysis.get_studies() == []:
                raise ValueError('Need at least one study to analyze.')

            metaAnalysis.set_metadata(self.get_arguments('metadataUse'))

            if metaAnalysis.get_metadata() == []:
                raise ValueError('Need at least one metadata selected.')

            metaAnalysis.set_datatypes(self.get_arguments('datatypeView'))

            if metaAnalysis.get_datatypes() == []:
                raise ValueError('Need at least one datatype selected.')

            # Add the combined datatype if more than one selected
            if len(metaAnalysis.get_datatypes()) > 1:
                metaAnalysis.add_datatype("Combined")

            self.render('meta2.html', user=self.user,
                        datatypes=metaAnalysis.get_datatypes(), single=SINGLE,
                        combined=COMBINED)

        elif page == '3':
            for datatype in metaAnalysis.get_datatypes():
                metaAnalysis.set_jobs(datatype, self.get_arguments(datatype))

            self.render('meta3.html', user=self.user,
                        analysisinfo=metaAnalysis)

        elif page == '4':
            #set options
            for datatype in metaAnalysis.get_datatypes():
                for analysis in metaAnalysis.get_jobs(datatype):
                    metaAnalysis.set_options(datatype, analysis,
                                             {'Option A': 'default',
                                              'Option B': 'default'})

            self.render('meta4.html', user=self.user,
                        analysisinfo=metaAnalysis)

        else:
            raise NotImplementedError("MetaAnalysis Page %s missing!" % page)


class NoPageHandler(BaseHandler):
    def get(self):
        self.render("404.html", user=self.get_current_user())


class Application(tornado.web.Application):
    def __init__(self, debug=False):
        dirname = dirname(__file__)
        static_path = join(dirname, 'static')
        template_path = join(dirname, 'templates')
        res_path = join(dirname, '../../support_files/results/')

        cookie = base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)

        handlers = [
            (r"/", MainHandler),
            (r"/auth/login/", AuthLoginHandler),
            (r"/auth/logout/", AuthLogoutHandler),
            (r"/auth/create/", AuthCreateHandler),
            (r"/results/(.*)", tornado.web.StaticFileHandler,
                {'path': res_path}),
            (r"/static/(.*)", tornado.web.StaticFileHandler,
                {'path': static_path}),
            (r"/waiting/(.*)", WaitingHandler),
            (r"/running/", RunningHandler),
            (r"/consumer/", MessageHandler),
            (r"/fileupload/", FileHandler),
            (r"/completed/(.*)", ShowJobHandler),
            (r"/meta/([0-9]+)", MetaAnalysisHandler),
            (r"/del/", DeleteAnalysisHandler),
            (r".*", NoPageHandler)  # It should be always the last one
        ]
        settings = {
            "template_path": template_path,
            "debug": debug,
            "cookie_secret": cookie,
            "login_url": "/auth/login/"
        }
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    print "Tornado started on port", options.port
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
