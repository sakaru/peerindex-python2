# Copyright 2013 PeerIndex, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
A Python interface for the PeerIndex API.

To use this you need a PeerIndex API key which 
    you can get at: http://dev.peerindex.com/

"""


from urllib import urlencode
from httplib import HTTPSConnection, HTTPException
import json

ERROR_STATUS = {
    # "200: "OK: Success", IS A GOOD STATUS
    202: "Accepted: Your request was accepted and the user was queued for processing.",
    401: "Not Authorized: either you need to provide authentication credentials, or the credentials provided aren't valid.",
    403: "Forbidden: Did you forget your developer key or exceed your allowance?",
    404: "Not Found: Most likely the profile doesn't exist."
}


class PeerIndexError(Exception):
    def __init__(self, code, msg):
        super(PeerIndexError, self).__init__()
        self.code = code
        self.msg = msg

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return '%i: %s' % (self.code, self.msg)


class PeerIndex(object):
    '''
    Parameters
    ----------
    api_key : string the PeerIndex API Key.

    '''
    API_URL = 'api.peerindex.com'
    API_VERSION = '1'

    def __init__(self, api_key):
        self._api_key = api_key

    def actorBasic(self, query):
        """
        Retrieve basic information about a user

        Parameters
        ----------
        query: A dict with ONE of the following keys: peerindex_id, twitter_screen_name, twitter_id

        Returns
        -------
        The returned actor object

        """
        url = 'actor/basic'
        data = self._make_api_call(url, query)
        return data

    def actorExtended(self, query):
        """
        Retrieve extended information about a user

        Parameters
        ----------
        query: A dict with ONE of the following keys: peerindex_id, twitter_screen_name, twitter_id

        Returns
        -------
        The returned actor object

        """
        url = 'actor/extended'
        data = self._make_api_call(url, query)
        return data

    def actorTopic(self, query):
        """
        Retrieve topic related information about a user

        Parameters
        ----------
        query: A dict with ONE of the following keys: peerindex_id, twitter_screen_name, twitter_id

        Returns
        -------
        The returned actor object

        """
        url = 'actor/topic'
        data = self._make_api_call(url, query)
        return data

    def actorGraph(self, query):
        """
        Retrieve the social graph of a user

        Parameters
        ----------
        query: A dict with ONE of the following keys: peerindex_id, twitter_screen_name, twitter_id

        Returns
        -------
        The returned actor object

        """
        url = 'actor/graph'
        data = self._make_api_call(url, query)
        return data

    def _remove_empty_params(self, params):
        '''
        Remove all unused parameters

        Parameters
        ----------
        params:  dict object
            A set of parameters key,value

        Returns
        --------
        The set of parameters as dict without empty parameters
        '''
        ret = {}
        for key in params:
            if params[key]:
                ret[key] = params[key]

        return ret

    def _make_api_call(self, url, query={}):
        '''
        Make the API Call to PeerIndex

        Parameters
        ----------
        url: the url to call
        query: The GET parameters
        '''

        url = '/' + self.API_VERSION + '/' + url
        query = self._remove_empty_params(query)

        if 'api_key' not in query:
            query['api_key'] = self._api_key

        query_str = urlencode(query)

        if len(query) > 0:
            if url.find('?') == -1:
                url = url + '?' + query_str
            else:
                url = url + '&' + query_str

        try:
            conn = HTTPSConnection(self.API_URL)
            conn.request('GET', url)
            resp = conn.getresponse()

            data = resp.read()
            data = json.loads(data)
            if not data:
                raise ValueError(data)
                
    
        except HTTPException as err:
            msg = err.read() or ERROR_STATUS.get(err.code, err.message)
            raise PeerIndexError(err.code, msg)

        return data
