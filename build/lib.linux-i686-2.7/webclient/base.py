'''This library provides basic webservice client python interfaces.'''

import httplib
import json
import sys
from urllib import urlencode

__author__ = 'Juan Enrique Munoz Zolotoochin'
__email__ = 'juanique@gmail.com'


class WebClient:

    def __init__(self, server, https=False, parser=json.loads, verbose=False):
        self.https = https
        self.server = server
        self.parser = parser
        self.verbose = verbose

    def _api_call(self, method, service, headers={}, **kwargs):
        '''Executes the HTTP request to the webservice and return
        the json-parsed response'''

        uri = "%s?%s" % (service, urlencode(kwargs))
        conn = self.get_connection()
        conn.request(method, uri, headers=headers)
        response = conn.getresponse()
        return response

    def get_connection(self):
        '''Return a connection object to the webservice.'''
        if self.https:
            conn_class = httplib.HTTPSConnection
        else:
            conn_class = httplib.HTTPConnection

        class Connection(conn_class):

            def __init__(self, verbose, *args, **kwargs):
                self.verbose = verbose
                self.response = None
                conn_class.__init__(self, *args, **kwargs)

            def _output(self, s):
                if self.verbose:
                    print ">%s" % s
                conn_class._output(self, s)

            def request(self, *args, **kwargs):
                conn_class.request(self, *args, **kwargs)
                self.response = conn_class.getresponse(self)

                if self.verbose:
                    for name, value in self.response.getheaders():
                        print "<%s : %s" % (name, value)
                    print "<status code: %s" % self.response.status

            def getresponse(self):
                return self.response

        return Connection(self.verbose, self.server)

    def get(self, service, headers={}, **kwargs):
        return self._api_call("GET", "/" + service, headers, **kwargs)

    def post(self, service, data="", headers={}, **kwargs):
        conn = self.get_connection()
        #conn.set_debuglevel(1)
        conn.request('POST', "/" + service, body=data, headers=headers)
        return conn.getresponse()


class WebClientException(Exception):
    pass
