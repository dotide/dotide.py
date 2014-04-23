from datetime import datetime
import json
from dotide.models import AccessToken, Datastream, Datapoint, Dataset


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

    def _build_access_token(self, json):
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
        return [self._build_access_token(token) for token in res]

    def create(self, scopes=None):
        """
        Create an AccessToken.
        """
        data = {}
        if scopes:
            data['scopes'] = scopes
        res = self._client.create_access_token(data=json.dumps(data))
        return self._build_access_token(res)

    def get(self, access_token):
        """
        Get an AccessToken.
        """
        res = self._client.read_access_token(access_token)
        return self._build_access_token(res)

    def update(self, access_token, scopes=None):
        """
        Update an AccessToken.
        """
        data = {}
        if scopes:
            data['scopes'] = scopes
        res = self._client.update_access_token(access_token,
                                               data=json.dumps(data))
        return self._build_access_token(res)

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

    def _build_datastream(self, json):
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
        return [self._build_datastream(datastream) for datastream in res]

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
        return self._build_datastream(res)

    def get(self, id):
        """
        Get a Datastream.
        """
        res = self._client.read_datastream(id)
        return self._build_datastream(res)

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
        return self._build_datastream(res)

    def delete(self, id):
        """
        Delete a datastream.
        """
        ret = self._client.delete_datastream(id)
        return ret is None


class DatapointManager(Manager):

    """
    Datapoint Manager.
    """

    def __init__(self, client, id):
        self._client = client
        self._id = id

    def _build_datapoint(self, json):
        return Datapoint(t=self._parse_datetime(json['t']),
                         v=json['v'])

    def _build_dataset(self, json):
        return Dataset(id=json['id'],
                       datapoints=json['datapoints'],
                       options=json.get('options', {}),
                       summary=json.get('summary', {}))

    def filter(self, start=None, end=None, order=None, t=None, limit=None,
               offset=None, summary=None, interval=None, function=None):
        """
        Filter Datapoints.
        """
        params = {k: v for k, v in (
            ('start', start),
            ('end', end),
            ('order', order),
            ('t', t),
            ('limit', limit),
            ('offset', offset),
            ('summary', summary),
            ('interval', interval),
            ('function', function),
        ) if v is not None}
        res = self._client.list_datapoints(self._id,
                                           params=self._format_params(params))
        res['datapoints'] = [self._build_datapoint(datapoint)
                             for datapoint in res['datapoints']]
        return self._build_dataset(res)

    def create(self, datapoints=None, t=None, v=None):
        """
        Create datapoint(s).
        """
        if datapoints:
            data = []
            for datapoint in datapoints:
                p = {}
                if 't' in datapoint:
                    p['t'] = datapoint['t'].isoformat()
                p['v'] = datapoint.get('v', None)
                data.append(p)
            res = self._client.create_datapoint(self._id, data=data)
            return [self._build_datapoint(datapoint) for datapoint in res]
        else:
            data = {'v': v}
            if t:
                data['t'] = t.isoformat()
            res = self._client.create_datapoint(self._id, data=data)
            return self._build_datapoint(res)

    def get(self, t):
        """
        Get datapoint by timestamp.
        """
        res = self._client.read_datapoint(self._id, t.isoformat())
        return self._build_datapoint(res)

    def delete(self, t=None, start=None, end=None):
        """
        Delete datapoints.
        """
        ret = False
        if t:
            ret = self._client.delete_datapoint(self._id, t.isoformat())
        elif start and end:
            ret = self._client.delete_datapoints(self._id,
                                                 start.isoformat(),
                                                 end.isoformat())
        return ret is None
