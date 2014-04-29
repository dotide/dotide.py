import requests
from requests.auth import HTTPBasicAuth
from dotide.managers import AccessTokenManager, DatastreamManager


class TokenAuth(requests.auth.AuthBase):

    """AccessToken Auth."""

    def __init__(self, access_token):
        self.access_token = access_token

    def __call__(self, r):
        r.headers['Authorization'] = 'Bearer ' + self.access_token
        return r


class Client(object):

    """Client. All API calls are made by this class.

    :param str database: Database's name.
    :param str client_id: Database's client_id.
    :param str client_secret: Database's client_secret.
    :param str access_token: Database's access_token.
    :param str host: Server's hostname, default 'api.dotide.com'.
    :param str version: API version, default 'v1'.
    :param bool secure: Whether use ssl, default True.

    Usage::

      >>> import dotide
      >>> client = dotide.Client('your_database_name', client_id='your_client_id', client_secret='your_client_secret')
    """

    def __init__(self,
                 database,
                 client_id=None,
                 client_secret=None,
                 access_token=None,
                 host='api.dotide.com',
                 version='v1',
                 secure=True):
        self.database = database  # : Database's name.
        self.client_id = client_id  # : Database's client_id.
        self.client_secret = client_secret  #: Database's client_secret.
        self.access_token = access_token  #: Database's access_token.
        self.host = host  #: Server's hostname.
        self.version = version  #: API version.
        self.secure = secure  #: Whether use ssl.
        self.session = requests.Session()
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'dotide.py',
            'TimeZone': 'UTC'
        }
        self.access_tokens = AccessTokenManager(self)
        self.datastreams = DatastreamManager(self)

    def _build_base_url(self):
        """Build base url."""
        schema = 'https' if self.secure else 'http'
        return '{schema}://{host}/{ver}/{db}'.format(schema=schema,
                                                     host=self.host,
                                                     ver=self.version,
                                                     db=self.database)

    def _build_full_url(self, target):
        """Build full url."""
        return self._build_base_url() + target

    def _build_auth(self):
        """Build auth."""
        if self.client_id and self.client_secret:
            auth = HTTPBasicAuth(self.client_id, self.client_secret)
        elif self.access_token:
            auth = TokenAuth(self.access_token)
        else:
            auth = None
        return auth

    def request(self, method, target, params=None, data=None):
        """An internal method that send request to server.
        It is exposed if you need to make API calls not implemented in this
        library or if you need to debug requests.

        :param str method: An HTTP method (e.g. 'GET' or 'POST').
        :param str target: The target URL with leading slash (e.g. '/datastreams').
        :param dict params: A dictionary of parameters to add to the request.
        :param str data: A json string. This is the body of the request.
        :returns: Parsed body.
        :rtype: dict or list.
        """
        r = self.session.request(method,
                                 self._build_full_url(target),
                                 params=params,
                                 data=data,
                                 headers=self.headers,
                                 auth=self._build_auth())

        data = r.json() if r.content else None
        if r.status_code >= 400:
            raise requests.exceptions.HTTPError(data['message'], response=r)
        return data

    def list_access_tokens(self, params=None):
        """List access_tokens."""
        return self.request('GET', '/access_tokens', params=params)

    def create_access_token(self, data=None):
        """Create an access_token."""
        return self.request('POST', '/access_tokens', data=data)

    def read_access_token(self, access_token):
        """Read an access_token."""
        return self.request('GET',
                            '/access_tokens/{access_token}'.format(
                                access_token=access_token))

    def update_access_token(self, access_token, data=None):
        """Update an access_token."""
        return self.request('PUT',
                            '/access_tokens/{access_token}'.format(
                                access_token=access_token),
                            data=data)

    def delete_access_token(self, access_token):
        """Delete an access_token."""
        return self.request('DELETE',
                            '/access_tokens/{access_token}'.format(
                                access_token=access_token))

    def list_datastreams(self, params=None):
        """List datastreams."""
        return self.request('GET', '/datastreams', params=params)

    def create_datastream(self, data=None):
        """Create an datastream."""
        return self.request('POST', '/datastreams', data=data)

    def read_datastream(self, id):
        """Read an datastream."""
        return self.request('GET', '/datastreams/{id}'.format(id=id))

    def update_datastream(self, id, data=None):
        """Update an datastream."""
        return self.request('PUT',
                            '/datastreams/{id}'.format(id=id),
                            data=data)

    def delete_datastream(self, id):
        """Delete an datastream."""
        return self.request('DELETE', '/datastreams/{id}'.format(id=id))

    def list_datapoints(self, id, params=None):
        """List datapoints."""
        return self.request('GET',
                            '/datastreams/{id}/datapoints'.format(id=id),
                            params=params)

    def create_datapoint(self, id, data=None):
        """Create datapoint(s)."""
        return self.request('POST',
                            '/datastreams/{id}/datapoints'.format(id=id),
                            data=data)

    def read_datapoint(self, id, t):
        """Read a datapoint by timestamp."""
        return self.request('GET',
                            '/datastreams/{id}/datapoints/{t}'.format(id=id,
                                                                      t=t))

    def delete_datapoints(self, id, start, end):
        """Delete a range of datapoints."""
        return self.request('DELETE',
                            '/datastreams/{id}/datapoints'.format(id=id),
                            params={'start': start, 'end': end})

    def delete_datapoint(self, id, t):
        """Delete datapoint by timestamp."""
        return self.request('DELETE',
                            '/datastreams/{id}/datapoints/{t}'.format(id=id,
                                                                      t=t))
