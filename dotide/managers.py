from datetime import datetime
from dotide.models import AccessToken, Datastream
import json


class Manager(object):

    """
    Abstract Manager.
    """

    def _parse_datetime(self, dt):
        """
        Parse iso8601 format UTC time to datetime.
        """
        return datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%fZ")

    def _format_params(self, params):
        """
        Format params.
        """
        new_params = {}
        for k, v in params.iteritems():
            if isinstance(v, list):
                new_params[k] = ','.join(v)
            elif isinstance(v, datetime):
                new_params[k] = v.isoformat()
            else:
                new_params[k] = v
        return new_params


class AccessTokenManager(Manager):

    """
    AccessToken Manager.
    """

    def __init__(self, client):
        self._client = client

    def _build_model(self, json):
        """
        Build AccessToken Model.
        """
        return AccessToken(manager=self,
                           access_token=json['access_token'],
                           scopes=json['scopes'],
                           created_at=self._parse_datetime(json['created_at']),
                           updated_at=self._parse_datetime(json['updated_at']))

    def filter(self):
        """
        Filter AccessTokens.
        """
        res = self._client.list_access_tokens()
        access_tokens = []
        for access_token in res:
            access_tokens.append(self._build_model(access_token))
        return access_tokens

    def create(self, scopes=None):
        """
        Create an AccessToken.
        """
        data = {}
        if scopes:
            data['scopes'] = scopes
        res = self._client.create_access_token(data=json.dumps(data))
        return self._build_model(res)

    def get(self, access_token):
        """
        Get an AccessToken.
        """
        res = self._client.read_access_token(access_token)
        return self._build_model(res)

    def update(self, access_token, scopes=None):
        """
        Update an AccessToken.
        """
        data = {}
        if scopes:
            data['scopes'] = scopes
        res = self._client.update_access_token(access_token,
                                               data=json.dumps(data))
        return self._build_model(res)

    def delete(self, access_token):
        """
        Delete an AccessToken.
        """
        ret = self._client.delete_access_token(access_token)
        return ret is None


class DatastreamManager(Manager):

    """
    Datastream Manager.
    """

    def __init__(self, client):
        self._client = client

    def _build_model(self, json):
        """
        Build Datastream Model.
        """
        return Datastream(manager=self,
                          id=json['id'],
                          name=json['name'],
                          type=json['type'],
                          tags=json['tags'],
                          properties=json['properties'],
                          current_t=self._parse_datetime(json['current_t']),
                          current_v=json['current_v'],
                          created_at=self._parse_datetime(json['created_at']),
                          updated_at=self._parse_datetime(json['updated_at']))

    def filter(self, ids=None, tags=None, limit=None, offset=None):
        """
        Filter Datastreams.
        """
        params = {k: v for k, v in (
            ('ids', ids),
            ('tags', tags),
            ('limit', limit),
            ('offset', offset),
        ) if v is not None}
        res = self._client.list_datastreams(params=self._format_params(params))
        datastreams = []
        for datastream in res:
            datastreams.append(self._build_model(datastream))
        return datastreams

    def create(self, id=None, name=None, type=None, tags=None,
               properties=None):
        """
        Create Datastream.
        """
        data = {k: v for k, v in (
            ('id', id),
            ('name', name),
            ('type', type),
            ('tags', tags),
            ('properties', properties),
        ) if v is not None}
        res = self._client.create_datastream(data=json.dumps(data))
        return self._build_model(res)

    def get(self, id):
        """
        Get a Datastream.
        """
        res = self._client.read_datastream(id)
        return self._build_model(res)

    def update(self, id, name=None, tags=None, properties=None):
        """
        Update a datastream.
        """
        data = {k: v for k, v in (
            ('name', name),
            ('tags', tags),
            ('properties', properties),
        ) if v is not None}
        res = self._client.update_datastream(id, data=json.dumps(data))
        return self._build_model(res)

    def delete(self, id):
        """
        Delete a datastream.
        """
        ret = self._client.delete_datastream(id)
        return ret is None
