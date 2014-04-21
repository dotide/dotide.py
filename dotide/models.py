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
