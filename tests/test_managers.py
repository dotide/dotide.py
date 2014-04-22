import unittest
import mock
import dotide
from dotide.managers import AccessTokenManager, DatastreamManager
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
        self.assertTrue(ret)


class TestDatastreamManager(unittest.TestCase):

    """Test for DatastreamManager"""

    def setUp(self):
        self.client = dotide.Client(client_id='id',
                                    client_secret='secret',
                                    database='db')
        self.client.request = mock.Mock()
        self.datastream_manager = DatastreamManager(self.client)
        self.datastream = {
            'id': '51e51544fa36a48592000074',
            'name': 'Demo Datastream',
            'type': 'number',
            'tags': ['a', 'b', 'c'],
            'properties': {
                'prop0': 'value0'
            },
            'current_t': '2014-01-03T00:01:02.123Z',
            'current_v': 100,
            'created_at': '2014-01-03T00:00:00.001Z',
            'updated_at': '2014-01-03T00:01:02.456Z'
        }

    def test_init(self):
        datastream_manager = DatastreamManager(self.client)
        self.assertIsInstance(datastream_manager, DatastreamManager)

    def test_filter(self):
        self.client.request.return_value = [self.datastream]
        datastreams = self.datastream_manager.filter(
            ids=[self.datastream['id']],
            tags=self.datastream['tags'])
        datastream = datastreams[0]
        self.assertEqual(datastream.id, self.datastream['id'])
        self.assertEqual(datastream.name, self.datastream['name'])
        self.assertEqual(datastream.type, self.datastream['type'])
        self.assertEqual(datastream.tags, self.datastream['tags'])
        self.assertEqual(datastream.properties, self.datastream['properties'])
        self.assertEqual(datastream.current_t,
                         datetime(2014, 1, 3, 0, 1, 2, 123000))
        self.assertEqual(datastream.current_v, self.datastream['current_v'])
        self.assertEqual(datastream.created_at,
                         datetime(2014, 1, 3, 0, 0, 0, 1000))
        self.assertEqual(datastream.updated_at,
                         datetime(2014, 1, 3, 0, 1, 2, 456000))

    def test_create(self):
        self.client.request.return_value = self.datastream
        datastream = self.datastream_manager.create(
            id=self.datastream['id'],
            name=self.datastream['name'],
            type=self.datastream['type'],
            tags=self.datastream['tags'],
            properties=self.datastream['properties'],
        )
        self.assertEqual(datastream.id, self.datastream['id'])
        self.assertEqual(datastream.name, self.datastream['name'])
        self.assertEqual(datastream.type, self.datastream['type'])
        self.assertEqual(datastream.tags, self.datastream['tags'])
        self.assertEqual(datastream.properties, self.datastream['properties'])
        self.assertEqual(datastream.current_t,
                         datetime(2014, 1, 3, 0, 1, 2, 123000))
        self.assertEqual(datastream.current_v, self.datastream['current_v'])
        self.assertEqual(datastream.created_at,
                         datetime(2014, 1, 3, 0, 0, 0, 1000))
        self.assertEqual(datastream.updated_at,
                         datetime(2014, 1, 3, 0, 1, 2, 456000))

    def test_get(self):
        self.client.request.return_value = self.datastream
        datastream = self.datastream_manager.get(self.datastream['id'])
        self.assertEqual(datastream.id, self.datastream['id'])
        self.assertEqual(datastream.name, self.datastream['name'])
        self.assertEqual(datastream.type, self.datastream['type'])
        self.assertEqual(datastream.tags, self.datastream['tags'])
        self.assertEqual(datastream.properties, self.datastream['properties'])
        self.assertEqual(datastream.current_t,
                         datetime(2014, 1, 3, 0, 1, 2, 123000))
        self.assertEqual(datastream.current_v, self.datastream['current_v'])
        self.assertEqual(datastream.created_at,
                         datetime(2014, 1, 3, 0, 0, 0, 1000))
        self.assertEqual(datastream.updated_at,
                         datetime(2014, 1, 3, 0, 1, 2, 456000))

    def test_update(self):
        self.client.request.return_value = self.datastream
        datastream = self.datastream_manager.get(self.datastream['id'])
        datastream.save()
        self.assertEqual(datastream.id, self.datastream['id'])
        self.assertEqual(datastream.name, self.datastream['name'])
        self.assertEqual(datastream.type, self.datastream['type'])
        self.assertEqual(datastream.tags, self.datastream['tags'])
        self.assertEqual(datastream.properties, self.datastream['properties'])
        self.assertEqual(datastream.current_t,
                         datetime(2014, 1, 3, 0, 1, 2, 123000))
        self.assertEqual(datastream.current_v, self.datastream['current_v'])
        self.assertEqual(datastream.created_at,
                         datetime(2014, 1, 3, 0, 0, 0, 1000))
        self.assertEqual(datastream.updated_at,
                         datetime(2014, 1, 3, 0, 1, 2, 456000))

    def test_delete(self):
        self.client.request.return_value = self.datastream
        datastream = self.datastream_manager.get(self.datastream['id'])
        self.client.request.return_value = None
        ret = datastream.delete()
        self.assertTrue(ret)

if __name__ == '__main__':
    unittest.main()
