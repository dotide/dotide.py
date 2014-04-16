import unittest
import dotide


class TestClient(unittest.TestCase):

    """Tests for Client."""

    def test_init_minimal(self):
        client = dotide.Client()
        self.assertIsNone(client.client_id)
        self.assertIsNone(client.client_secret)
        self.assertIsNone(client.access_token)
        self.assertIsNone(client.database)

    def test_init_with_client_id_secret_db(self):
        client_id = 'id'
        client_secret = 'secret'
        db = 'db'
        client = dotide.Client(client_id=client_id,
                               client_secret=client_secret,
                               database=db)
        self.assertEqual(client.client_id, 'id')
        self.assertEqual(client.client_secret, 'secret')
        self.assertIsNone(client.access_token)
        self.assertEqual(client.database, 'db')


if __name__ == '__main__':
    unittest.main()
