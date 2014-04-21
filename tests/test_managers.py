import unittest
import mock
import dotide
from dotide.managers import AccessTokenManager
from datetime import datetime


class TestAccessTokenManager(unittest.TestCase):

    """Test for AccessTokenManager"""

    def setUp(self):
        self.client = dotide.Client(client_id='id',
                                    client_secret='secret',
                                    database='db')
        self.client.request = mock.Mock()
        self.access_token_manager = AccessTokenManager(self.client)
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

    def test_init(self):
        access_token_manager = AccessTokenManager(self.client)
        self.assertIsInstance(access_token_manager, AccessTokenManager)

    def test_filter(self):
        self.client.request.return_value = [self.access_token]
        access_tokens = self.access_token_manager.filter()
        access_token = access_tokens[0]
        self.assertEqual(access_token.access_token,
                         self.access_token['access_token'])
        self.assertEqual(access_token.scopes, self.access_token['scopes'])
        self.assertEqual(access_token.created_at,
                         datetime(2014, 3, 1, 16, 59, 48, 455000))
        self.assertEqual(access_token.updated_at,
                         datetime(2014, 3, 1, 17, 1, 6, 690000))

    def test_create(self):
        self.client.request.return_value = self.access_token
        access_token = self.access_token_manager.create(
            scopes=self.access_token['scopes'])
        self.assertEqual(access_token.access_token,
                         self.access_token['access_token'])
        self.assertEqual(access_token.scopes, self.access_token['scopes'])
        self.assertEqual(access_token.created_at,
                         datetime(2014, 3, 1, 16, 59, 48, 455000))
        self.assertEqual(access_token.updated_at,
                         datetime(2014, 3, 1, 17, 1, 6, 690000))

    def test_get(self):
        self.client.request.return_value = self.access_token
        access_token = self.access_token_manager.get(
            self.access_token['access_token'])
        self.assertEqual(access_token.access_token,
                         self.access_token['access_token'])
        self.assertEqual(access_token.scopes, self.access_token['scopes'])
        self.assertEqual(access_token.created_at,
                         datetime(2014, 3, 1, 16, 59, 48, 455000))
        self.assertEqual(access_token.updated_at,
                         datetime(2014, 3, 1, 17, 1, 6, 690000))

    def test_update(self):
        self.client.request.return_value = self.access_token
        access_token = self.access_token_manager.get(
            self.access_token['access_token'])
        access_token.save()
        self.assertEqual(access_token.access_token,
                         self.access_token['access_token'])
        self.assertEqual(access_token.scopes, self.access_token['scopes'])
        self.assertEqual(access_token.created_at,
                         datetime(2014, 3, 1, 16, 59, 48, 455000))
        self.assertEqual(access_token.updated_at,
                         datetime(2014, 3, 1, 17, 1, 6, 690000))

    def test_delete(self):
        self.client.request.return_value = self.access_token
        access_token = self.access_token_manager.get(
            self.access_token['access_token'])
        self.client.request.return_value = None
        ret = access_token.delete()
        self.assertEqual(ret, True)
