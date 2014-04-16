class Client(object):

    """
    Client. All API calls are made by this class.
    """

    def __init__(self,
                 client_id=None,
                 client_secret=None,
                 access_token=None,
                 database=None):
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
