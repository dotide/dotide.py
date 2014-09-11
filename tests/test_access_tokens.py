import unittest
import mock
import json
from dotide import Dotide
from .helper import mock_response


class TestAccessTokens(unittest.TestCase):

    """Tests for datastreams."""

    def setUp(self):
        self.client = Dotide(database='db',
                             client_id='id',
                             client_secret='secret')
        self.client.client.session = mock.Mock()
        self.access_token = {
            'access_token': '61e13e47ed0b1b6f6a0ebe598d5ddba0c386a0d856487ec84\
                e973d06b1848221',
            'scopes': [{
                'permissions': ['read', 'write', 'delete'],
                'global': True,
                'ids': [],
                'tags': []
            }],
            'created_at': '2014-03-01T16:59:48.455Z',
            'updated_at': '2014-03-01T17:01:06.690Z'
        }

    def test_filter(self):
        self.client.client.session.request.return_value = mock_response(
            200, json.dumps([self.access_token]))
        access_tokens = self.client.access_tokens.filter()
        self.assertEqual(access_tokens, [self.access_token])

    def test_create(self):
        self.client.client.session.request.return_value = mock_response(
            201, json.dumps(self.access_token))
        access_token = self.client.access_tokens.create(self.access_token)
        self.assertEqual(access_token, self.access_token)

    def test_get(self):
        self.client.client.session.request.return_value = mock_response(
            200, json.dumps(self.access_token))
        access_token = self.client.access_tokens.get(self.access_token['access_token'])
        self.assertEqual(access_token, self.access_token)

    def test_update(self):
        self.client.client.session.request.return_value = mock_response(
            200, json.dumps(self.access_token))
        access_token = self.client.access_tokens.update(self.access_token['access_token'],
                                                    self.access_token)
        self.assertEqual(access_token, self.access_token)

    def test_delete(self):
        self.client.client.session.request.return_value = mock_response(204)
        ret = self.client.access_tokens.delete(self.access_token['access_token'])
        self.assertEqual(True, ret)


if __name__ == '__main__':
    unittest.main()
