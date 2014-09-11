import unittest
from dotide.client import Client


class TestClient(unittest.TestCase):

    """Tests for Client."""

    def setUp(self):
        self.client = Client(client_id='id',
                             client_secret='secret',
                             database='db')

    def test_init_minimal(self):
        client = Client('db')
        self.assertEqual(client.database, 'db')
        self.assertIsNone(client.client_id)
        self.assertIsNone(client.client_secret)
        self.assertIsNone(client.access_token)

    def test_init_with_client_id_secret_db(self):
        client_id = 'id'
        client_secret = 'secret'
        db = 'db'
        client = Client(db,
                        client_id=client_id,
                        client_secret=client_secret)
        self.assertEqual(client.database, 'db')
        self.assertEqual(client.client_id, 'id')
        self.assertEqual(client.client_secret, 'secret')
        self.assertIsNone(client.access_token)


if __name__ == '__main__':
    unittest.main()
