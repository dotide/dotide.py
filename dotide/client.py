import requests
from requests.auth import HTTPBasicAuth


class TokenAuth(requests.auth.AuthBase):

    """
    AccessToken Auth.
    """

    def __init__(self, access_token):
        self.access_token = access_token

    def __call__(self, r):
        r.headers['Authorization'] = 'Bearer ' + self.access_token
        return r


class Client(object):

    """
    Client. All API calls are made by this class.
    """

    def __init__(self,
                 client_id=None,
                 client_secret=None,
                 access_token=None,
                 database=None,
                 host='api.dotide.com',
                 version='v1',
                 secure=True):
        """
        Construct a `Client` instance.

        Parameters
            client_id
                Database's client_id.
            client_secret
                Database's client_secret.
            access_token
                Database's access_token.
            database
                Database's name.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.database = database
        self.host = host
        self.version = version
        self.secure = secure
        self.session = requests.Session()
        self.headers = {'Content-Type': 'application/json',
                        'User-Agent': 'dotide.py',
                        'TimeZone': 'UTC'}

    def build_base_url(self):
        """
        Build base url
        """
        schema = 'https' if self.secure else 'http'
        return '{schema}://{host}/{ver}/{db}'.format(schema=schema,
                                                     host=self.host,
                                                     ver=self.version,
                                                     db=self.database)

    def build_full_url(self, target):
        """
        Build full url.
        """
        return self.build_base_url() + target

    def build_auth(self):
        """
        Build auth.
        """
        if self.client_id and self.client_secret:
            auth = HTTPBasicAuth(self.client_id, self.client_secret)
        elif self.access_token:
            auth = TokenAuth(self.access_token)
        else:
            auth = None
        return auth

    def request(self, method, target, params=None, data=None):
        """
        An internal method that send request to server.
        It is exposed if you need to make API calls not implemented in this
        library or if you need to debug requests.

        Parameters
            method
                An HTTP method (e.g. 'GET' or 'POST').
            target
                The target URL with leading slash (e.g. '/datastreams').
            params
                A dictionary of parameters to add to the request.
            data
                A json string. This is the body of the request.

        Returns
            parsed body
        """
        r = self.session.request(method,
                                 self.build_full_url(target),
                                 params=params,
                                 data=data,
                                 headers=self.headers,
                                 auth=self.build_auth())

        data = r.json() if r.content else None
        if r.status_code >= 400:
            raise requests.exceptions.HTTPError(data['message'] ,response=r)
        return data

    def list_access_tokens(self, params=None):
        """
        List access_tokens.
        """
        return self.request('GET', '/access_tokens', params=params)

    def create_access_token(self, data=None):
        """
        Create an access_token.
        """
        return self.request('POST', '/access_tokens', data=data)

    def read_access_token(self, access_token):
        """
        Read an access_token.
        """
        return self.request('GET', '/access_tokens/' + access_token)

    def update_access_token(self, access_token, data=None):
        """
        Update an access_token.
        """
        return self.request('PUT', '/access_tokens/' + access_token, data=data)

    def delete_access_token(self, access_token):
        """
        Delete an access_token.
        """
        return self.request('DELETE', '/access_tokens/' + access_token)

    def list_datastreams(self, params=None):
        """
        List datastreams.
        """
        return self.request('GET', '/datastreams', params = params)

    def create_datastream(self, data=None):
        """
        Create an datastream.
        """
        return self.request('POST', '/datastreams', data=data)

    def read_datastream(self, id):
        """
        Read an datastream.
        """
        return self.request('GET', '/datastreams/' + id)

    def update_datastream(self, id, data=None):
        """
        Update an datastream.
        """
        return self.request('PUT', '/datastreams/' + id, data=data)

    def delete_datastream(self, id):
        """
        Delete an datastream.
        """
        return self.request('DELETE', '/datastreams/' + id)
