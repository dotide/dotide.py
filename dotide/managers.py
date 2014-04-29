from datetime import datetime
import json
from dotide.models import AccessToken, Datastream, Datapoint, Dataset


class Manager(object):

    """Abstract Manager."""

    def _parse_datetime(self, dt):
        """Parse iso8601 format UTC time to datetime."""
        return datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S.%fZ")

    def _format_params(self, params):
        """Format params."""
        def _coerce(v):
            if isinstance(v, list):
                return ','.join(v)
            elif isinstance(v, datetime):
                return v.isoformat()
            else:
                return v
        return {k: _coerce(params[k]) for k in params}


class AccessTokenManager(Manager):

    """AccessToken Manager."""

    def __init__(self, client):
        self._client = client

    def _build_access_token(self, json):
        """Build AccessToken Model."""
        return AccessToken(manager=self,
                           access_token=json['access_token'],
                           scopes=json['scopes'],
                           created_at=self._parse_datetime(json['created_at']),
                           updated_at=self._parse_datetime(json['updated_at']))

    def filter(self):
        """Filter AccessTokens.

        :returns: List of AccessTokens.

        Usage::

            >>> access_tokens = client.access_tokens.filter()
        """
        res = self._client.list_access_tokens()
        return [self._build_access_token(token) for token in res]

    def create(self, scopes=None):
        """Create an AccessToken.

        :param list scopes: AccessToken's effect scopes.
        :returns: Created AccessToken instance.

        Usage::

            >>> access_token = client.access_tokens.create(scopes=[{
                                                           'permissions': ['read', 'write', 'delete'],
                                                           'global': False,
                                                           'ids': ['id0'],
                                                           'tags': ['tag0']
                                                           }])
        """
        data = {}
        if scopes:
            data['scopes'] = scopes
        res = self._client.create_access_token(data=json.dumps(data))
        return self._build_access_token(res)

    def get(self, access_token):
        """Get an AccessToken.

        :param str access_token: AccessToken's access_token.
        :returns: AccessToken instance.

        Usage::

            >>> access_token = client.access_tokens.get('your_access_token')
        """
        res = self._client.read_access_token(access_token)
        return self._build_access_token(res)

    def update(self, access_token, scopes=None):
        """Update an AccessToken."""
        data = {}
        if scopes:
            data['scopes'] = scopes
        res = self._client.update_access_token(access_token,
                                               data=json.dumps(data))
        return self._build_access_token(res)

    def delete(self, access_token):
        """Delete an AccessToken."""
        ret = self._client.delete_access_token(access_token)
        return ret is None


class DatastreamManager(Manager):

    """Datastream Manager."""

    def __init__(self, client):
        self._client = client

    def _build_datastream(self, json):
        """Build Datastream Model."""
        t = json['current_t']
        current_t = self._parse_datetime(t) if t else None
        return Datastream(manager=self,
                          id=json['id'],
                          name=json['name'],
                          type=json['type'],
                          tags=json['tags'],
                          properties=json['properties'],
                          current_t=current_t,
                          current_v=json['current_v'],
                          created_at=self._parse_datetime(json['created_at']),
                          updated_at=self._parse_datetime(json['updated_at']))

    def filter(self, ids=None, tags=None, limit=None, offset=None):
        """Filter Datastreams.

        :param list ids: Datastream id list.
        :param list tags: Datastream tag list.
        :param int limit: Results amount limit.
        :param int offset: Results offset amount.
        :returns: List of Datastreams.

        Usage::

            >>> datastreams = client.datastreams.filter(ids=['id0', 'id1'],
                                                        tags=['tag0', 'tag1'],
                                                        limit=10,
                                                        offset=10
                                                        )
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
        """Create Datastream.

        :param str id: Datastream's id.
        :param str name: Datastream's name.
        :param str type: Datastream's type.
        :param list tags: Datastream's tags.
        :param dict properties: Datastream's properties.
        :returns: Created Datastream instance.

        Usage::

            >>> datastream = client.datastreams.create(id='id0',
                                                       name='name0',
                                                       type='number',
                                                       tags=['tag0'],
                                                       proerties={'prop0': 1}
                                                       )
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
        """Get a Datastream.

        :param str id: Datastream's id.
        :returns: Datastream instance.

        Usage::

            >>> datastream = client.datastreams.get('id0')
        """
        res = self._client.read_datastream(id)
        return self._build_datastream(res)

    def update(self, id, name=None, tags=None, properties=None):
        """Update a datastream."""
        data = {k: v for k, v in (
            ('name', name),
            ('tags', tags),
            ('properties', properties),
        ) if v is not None}
        res = self._client.update_datastream(id, data=json.dumps(data))
        return self._build_datastream(res)

    def delete(self, id):
        """Delete a datastream."""
        ret = self._client.delete_datastream(id)
        return ret is None


class DatapointManager(Manager):

    """Datapoint Manager."""

    def __init__(self, client, id):
        self._client = client
        self._id = id

    def _build_datapoint(self, json):
        """Build Datapoint Model."""
        return Datapoint(t=self._parse_datetime(json['t']),
                         v=json['v'])

    def _build_dataset(self, json):
        """Build Dataset Model."""
        return Dataset(id=json['id'],
                       datapoints=json['datapoints'],
                       options=json.get('options', {}),
                       summary=json.get('summary', {}))

    def filter(self, start=None, end=None, order=None, t=None, limit=None,
               offset=None, summary=None, interval=None, function=None):
        """Filter Datapoints.

        :param datetime start: Start time.
        :param datetime end: End time.
        :param str order: Order asc or desc.
        :param datetime t: Exactly time.
        :param int limit: Results amount limit.
        :param int offset: Results offset amount.
        :param int summary: Whether contain summary in output, 0 or 1.
        :param int interval: Sampling interval in ms.
        :param str function: Sampling function.
        :returns: Dataset instance.

        Usage::

            >>> dataset = datastream.datapoints.filter(start=datetime(2014, 1, 1),
                                                       end=datetime.utcnow(),
                                                       order='asc',
                                                       limit=1000)
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
        """Create datapoint(s).

        :param list datapoints: List of datapoints.
        :param datetime t: Time.
        :param v: Value.
        :returns: Created datapoint(s).

        Usage::

            >>> datapoint = datastream.datapoints.create(t=datetime.utcnow(), v=1)
            >>> datapoints = datastream.datapoints.create([{'t': datetime.utcnow(),
                                                          'v': 1}])
        """
        if datapoints:
            data = []
            for datapoint in datapoints:
                p = {}
                if 't' in datapoint:
                    p['t'] = datapoint['t'].isoformat()
                p['v'] = datapoint.get('v', None)
                data.append(p)
            res = self._client.create_datapoint(self._id,
                                                data=json.dumps(data))
            return [self._build_datapoint(datapoint) for datapoint in res]
        else:
            data = {'v': v}
            if t:
                data['t'] = t.isoformat()
            res = self._client.create_datapoint(self._id,
                                                data=json.dumps(data))
            return self._build_datapoint(res)

    def get(self, t):
        """Get datapoint by timestamp.

        :param datetime t: Time.
        :returns: Datapoint instance.

        Usage::

            >>> datapoint = datastream.datapoints.get(datetime(2014, 1, 2, 3, 4, 5, 6000))
        """
        res = self._client.read_datapoint(self._id, t.isoformat())
        return self._build_datapoint(res)

    def delete(self, t=None, start=None, end=None):
        """Delete datapoints.

        :param datetime t: Exactly time.
        :param datetime start: Start time.
        :param datetime end: End time.
        :returns: True if success. Else False.

        Usage::

            >>> datastream.datapoints.delete(datetime(2014, 1, 2, 3, 4, 5, 6000))
            >>> datastream.datapoints.delete(start=datetime(2014, 1, 1),
                                             end=datetime.utcnow())
        """
        ret = False
        if t:
            ret = self._client.delete_datapoint(self._id, t.isoformat())
        elif start and end:
            ret = self._client.delete_datapoints(self._id,
                                                 start.isoformat(),
                                                 end.isoformat())
        return ret is None
