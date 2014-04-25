import dotide.managers


class AccessToken(object):

    """AccessToken Model."""

    def __init__(self, manager=None, access_token=None, scopes=None,
                 created_at=None, updated_at=None):
        self._manager = manager
        self.access_token = access_token  #: AccessToken's access_token string.
        self.created_at = created_at  #: AccessToken's create time.
        self.updated_at = updated_at  #: AccessToken's update time.
        self.scopes = []  #: AccessToken's effect scopes.
        if scopes:
            for scope in scopes:
                self.scopes.append({
                                   'permissions': scope.get('permissions', []),
                                   'global': scope.get('global', False),
                                   'ids': scope.get('ids', []),
                                   'tags': scope.get('tags', [])
                                   })

    def save(self):
        """Update AccessToken.

        Usage::

            >>> access_token.save()
        """
        access_token = self._manager.update(self.access_token,
                                            scopes=self.scopes)
        self.updated_at = access_token.updated_at
        return self

    def delete(self):
        """Delete AccessToken.

        Usage::

            >>> access_token.delete()
        """
        return self._manager.delete(self.access_token)


class Datastream(object):

    """Datastream Model."""

    def __init__(self, manager=None, id=None, name=None, type=None, tags=None,
                 properties=None, current_t=None, current_v=None,
                 created_at=None, updated_at=None):
        self._manager = manager
        self.id = id  #: Datastream's id.
        self.name = name  #: Datastream's name.
        self.type = type  #: Datastream's type.
        self.tags = tags  #: Datastream's tags.
        self.properties = properties  #: Datastream's properties.
        self.current_t = current_t  #: Datastream's latest datapoint's t
        self.current_v = current_v  #: Datastream's latest datapoint's v
        self.created_at = created_at  #: Datastream's create time.
        self.updated_at = updated_at  #: Datastream's update time.
        if manager and id is not None:
            self.datapoints = dotide.managers.DatapointManager(manager._client,
                                                               id)

    def save(self):
        """Update Datastream.

        Usage::

            >>> datastream.save()
        """
        datastream = self._manager.update(self.id,
                                          name=self.name,
                                          tags=self.tags,
                                          properties=self.properties)
        self.updated_at = datastream.updated_at
        return self

    def delete(self):
        """Delete Datastream.

        Usage::

            >>> datastream.delete()
        """
        return self._manager.delete(self.id)


class Datapoint(object):

    """Datapoint Model."""

    def __init__(self, t=None, v=None):
        self.t = t  #: Datapoint's time.
        self.v = v  #: Datapoint's value.


class Dataset(object):

    """Dataset Model."""

    def __init__(self, id=None, datapoints=None, options=None, summary=None):
        self.id = id  #: Datastream's id.
        self.datapoints = datapoints  #: List of datapoints
        self.options = options  #: Dict of options
        self.summary = summary  #: Dict of summary
