from datetime import datetime
from dotide.models import AccessToken
import json


class AccessTokenManager(object):

    """
    AccessToken Manager.
    """

    def __init__(self, client):
        self._client = client

    def _parse_datetime(self, dt):
        """
        Parse iso8601 format UTC time to datetime.
        """
        return datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%fZ")

    def _build_model(self, json):
        return AccessToken(manager=self,
                           access_token=json['access_token'],
                           scopes=json['scopes'],
                           created_at=self._parse_datetime(json['created_at']),
                           updated_at=self._parse_datetime(json['updated_at']))

    def filter(self):
        res = self._client.list_access_tokens()
        access_tokens = []
        for access_token in res:
            access_tokens.append(self._build_model(access_token))
        return access_tokens

    def create(self, scopes=None):
        data = {}
        if scopes:
            data['scopes'] = scopes
        res = self._client.create_access_token(data=json.dumps(data))
        return self._build_model(res)

    def get(self, access_token):
        res = self._client.read_access_token(access_token)
        return self._build_model(res)

    def update(self, access_token, scopes=None):
        data = {}
        if scopes:
            data['scopes'] = scopes
        res = self._client.update_access_token(access_token,
                                               data=json.dumps(data))
        return self._build_model(res)

    def delete(self, access_token):
        ret = self._client.delete_access_token(access_token)
        print ret
        if ret is None:
            return True
        else:
            return False

