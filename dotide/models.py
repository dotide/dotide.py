import dotide.managers


class AccessToken(object):

    """
    AccessToken Model.
    """

    def __init__(self, manager=None, access_token=None, scopes=None,
                 created_at=None, updated_at=None):
        self._manager = manager
        self.access_token = access_token
        self.created_at = created_at
        self.updated_at = updated_at
        self.scopes = []
        if scopes:
            for scope in scopes:
                self.scopes.append({
                                   'permissions': scope.get('permissions', []),
                                   'global': scope.get('global', False),
                                   'ids': scope.get('ids', []),
                                   'tags': scope.get('tags', [])
                                   })

    def save(self):
        access_token = self._manager.update(self.access_token,
                                            scopes=self.scopes)
        self.updated_at = access_token.updated_at
        return self

    def delete(self):
        return self._manager.delete(self.access_token)


class Datastream(object):

    """
    Datastream Model.
    """

    def __init__(self, manager=None, id=None, name=None, type=None, tags=None,
                 properties=None, current_t=None, current_v=None,
                 created_at=None, updated_at=None):
        self._manager = manager
        self.id = id
        self.name = name
        self.type = type
        self.tags = tags
        self.properties = properties
        self.current_t = current_t
        self.current_v = current_v
        self.created_at = created_at
        self.updated_at = updated_at
        if manager and id is not None:
            self.datapoints = dotide.managers.DatapointManager(manager._client,
                                                               id)

    def save(self):
        datastream = self._manager.update(self.id,
                                          name=self.name,
                                          tags=self.tags,
                                          properties=self.properties)
        self.updated_at = datastream.updated_at
        return self

    def delete(self):
        return self._manager.delete(self.id)


class Datapoint(object):

    """
    Datapoint Model.
    """

    def __init__(self, t=None, v=None):
        self.t = t
        self.v = v


class Dataset(object):

    """
    Dataset Model.
    """

    def __init__(self, id=None, datapoints=None, options=None, summary=None):
        self.id = id
        self.datapoints = datapoints
        self.options = options
        self.summary = summary
