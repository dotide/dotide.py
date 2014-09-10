import unittest
from dotide import Dotide


class TestDotide(unittest.TestCase):

    """Tests for TestDotide."""

    def test_init_minimal(self):
        client = Dotide('db')
        self.assertEqual(client.client.database, 'db')
        self.assertIsNotNone(client.datastreams)
        self.assertIsNotNone(client.datapoints)
        self.assertIsNotNone(client.access_tokens)

    def test_init_with_client_id_secret_db(self):
        client = Dotide('db',
                        client_id='id',
                        client_secret='secret')
        self.assertEqual(client.client.database, 'db')
        self.assertEqual(client.client.client_id, 'id')
        self.assertEqual(client.client.client_secret, 'secret')
        self.assertIsNone(client.client.access_token)
        self.assertIsNotNone(client.datastreams)
        self.assertIsNotNone(client.datapoints)
        self.assertIsNotNone(client.access_tokens)

    def test_init_with_access_token(self):
        client = Dotide('db', access_token='token')
        self.assertEqual(client.client.database, 'db')
        self.assertEqual(client.client.access_token, 'token')
        self.assertIsNone(client.client.client_id)
        self.assertIsNone(client.client.client_secret)
        self.assertIsNotNone(client.datastreams)
        self.assertIsNotNone(client.datapoints)
        self.assertIsNotNone(client.access_tokens)


if __name__ == '__main__':
    unittest.main()
