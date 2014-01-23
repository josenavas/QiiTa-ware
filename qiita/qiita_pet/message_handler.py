#!/usr/bin/env python

__author__ = "Joshua Shorenstein"
__copyright__ = "Copyright 2013, The QiiTa-pet Project"
__credits__ = ["Joshua Shorenstein", "Jose Antonio Navas Molina"]
__license__ = "BSD"
__version__ = "0.2.0-dev"
__maintainer__ = "Joshua Shorenstein"
__email__ = "Joshua.Shorenstein@colorado.edu"
__status__ = "Development"

# Adapted from
# https://github.com/leporo/tornado-redis/blob/master/demos/websockets

from tornadoredis import Client
from qiita.qiita_ware.connections import r_server
from tornado.websocket import WebSocketHandler
import tornado.gen
from json import loads


class MessageHandler(WebSocketHandler):
    def __init__(self, *args, **kwargs):
        super(MessageHandler, self).__init__(*args, **kwargs)
        self.redis = Client()
        self.redis.connect()

    def get_current_user(self):
        user = self.get_secure_cookie("user")
        if user is None:
            return ''
        else:
            return user.strip('" ')

    def on_message(self, msg):
        msginfo = loads(msg)
        #listens for handshake from page
        if "user:" in msginfo['msg']:
            self.channel = msginfo['msg'].split(':')[1]
            #need to split the rest off to new func so it can be asynchronous
            self.listen()

    # Decorator turns the function into an asynchronous generator object
    @tornado.gen.engine
    def listen(self):
        #runs task given, with the yield required to get returned value
        #equivalent of callback/wait pairing from tornado.gen
        yield tornado.gen.Task(self.redis.subscribe, self.channel)
        if not self.redis.subscribed:
            self.write_message('ERROR IN SUBSCRIPTION')
        #listen from tornadoredis makes the listen object asynchronous
        #if using standard redis lib, it blocks while listening
        self.redis.listen(self.callback)
        # Try and fight race condition by loading from redis after listen
        # started need to use std redis lib because tornadoredis is in
        # subscribed state
        old_messages = r_server.lrange(self.channel + ':messages', 0, -1)
        if old_messages is not None:
            for message in old_messages:
                self.write_message(message)

    def callback(self, msg):
        if msg.kind == 'message':
            self.write_message(str(msg.body))

    @tornado.gen.engine
    def on_close(self):
        yield tornado.gen.Task(self.redis.unsubscribe, self.channel)
        self.redis.disconnect()
