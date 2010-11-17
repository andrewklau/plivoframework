# -*- coding: utf-8 -*-
"""
Event Types classes
"""

from urllib import unquote
from urllib import quote


class Event(object):
    '''Event class'''
    def __init__(self, buffer=""):
        self._headers = {}
        self._body = ''
        if buffer:
            # Sets event headers from buffer.
            for line in buffer.splitlines():
                try:
                    var, val = line.rstrip().split(': ', 1)
                    var = var.strip()
                    val = unquote(val.strip())
                    self.set_header(var, val)
                except ValueError: 
                    pass

    def __getitem__(self, key):
        return self.get_header(key)

    def __setitem__(self, key, value):
        self.set_header(key, value)

    def get_content_length(self):
        '''
        Gets Content-Length header as integer.

        Returns 0 If length not found.
        '''
        length = self.get_header('Content-Length')
        if length:
            try:
                return int(length)
            except:
                return 0
        return 0

    def get_reply_text(self):
        '''
        Gets Reply-Text header as string.

        Returns None if header not found.
        '''
        return self.get_header('Reply-Text') 

    def is_reply_text_success(self):
        '''
        Returns True if ReplyText header begins with +OK.
        
        Returns False otherwise.
        '''
        reply = self.get_reply_text()
        return reply and reply[:3] == '+OK'

    def get_content_type(self):
        '''
        Gets Content-Type header as string.

        Returns None if header not found.
        '''
        return self.get_header('Content-Type')

    def get_headers(self):
        '''
        Gets all headers as a python dict.
        '''
        return self._headers

    def set_headers(self, headers):
        '''
        Sets all headers from dict.
        '''
        self._headers = headers.copy()

    def get_header(self, key, defaultvalue=None):
        '''
        Gets a specific header as string.

        Returns None if header not found.
        '''
        try:
            return self._headers[key]
        except KeyError:
            return defaultvalue

    def set_header(self, key, value):
        '''
        Sets a specific header.
        '''
        self._headers[key] = value

    def get_body(self):
        '''
        Gets Event body.
        '''
        return self._body

    def set_body(self, data):
        '''
        Sets Event body.
        '''
        self._body = data

    def get_raw_event(self):
        raw = ''
        raw += '\n'.join([ '%s: %s' % (k, quote(v)) for k, v in self.get_headers().iteritems() ])
        raw += '\n'
        if self._body:
            raw += self._body
        return raw

    def __str__(self):
        return '<Event [headers=%s, response=%s]>' \
               % (str(self.get_headers()), str(self.get_body()))



class ApiResponse(Event):
    def __init__(self, buffer=""):
        Event.__init__(self, buffer)

    @classmethod
    def cast(self, event):
        '''
        Makes an ApiResponse instance from Event instance.
        '''
        cls = ApiResponse()
        cls.set_headers(event.get_headers())
        cls.set_body(event.get_body())
        return cls

    def get_response(self):
        '''
        Gets response for api command.
        '''
        return self.get_body()

    def is_success(self):
        '''
        Returns True if api command is a success.
        
        Otherwise returns False.
        '''
        return self._body and self._body[:3] == '+OK'

    def __str__(self):
        return '<ApiResponse [headers=%s, response=%s]>' \
               % (str(self.get_headers()), str(self.get_response()))



class BgapiResponse(Event):
    def __init__(self, buffer=""):
        Event.__init__(self, buffer)
        self._background_job = None

    @classmethod
    def cast(self, event):
        '''
        Makes a BgapiResponse instance from Event instance.
        '''
        cls = BgapiResponse()
        cls.set_headers(event.get_headers())
        cls.set_body(event.get_body())
        return cls

    def get_response(self):
        '''
        Gets response for bgapi command.
        '''
        return self.get_reply_text()

    def get_job_uuid(self):
        '''
        Gets Job-UUID from bgapi command.
        '''
        return self.get_header('Job-UUID')

    def is_success(self):
        '''
        Returns True if bgapi command is a success.
        
        Otherwise returns False.
        '''
        return self.is_reply_text_success()

    def __str__(self):
        return '<BgapiResponse [headers=%s, response=%s, jobuuid=%s]>' \
               % (str(self.get_headers()), str(self.get_response()), self.get_job_uuid())



class CommandResponse(Event):
    def __init__(self, buffer=""):
        Event.__init__(self, buffer)

    @classmethod
    def cast(self, event):
        '''
        Makes a CommandResponse instance from Event instance.
        '''
        cls = CommandResponse()
        cls.set_headers(event.get_headers())
        cls.set_body(event.get_body())
        return cls

    def get_response(self):
        '''
        Gets response for a command.
        '''
        return self.get_reply_text()

    def is_success(self):
        '''
        Returns True if command is a success.
        
        Otherwise returns False.
        '''
        return self.is_reply_text_success()

    def __str__(self):
        return '<CommandResponse [headers=%s, response=%s]>' \
               % (str(self.get_headers()), str(self.get_response()))


