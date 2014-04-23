import unittest
import mock
import requests
import json
import dotide


def mock_response(status_code=200, content=None):
    r = requests.Response()
    r.status_code = status_code
    r._content = content
    return r


class TestClient(unittest.TestCase):

    """Tests for Client."""

    def setUp(self):
        self.client = dotide.Client(client_id='id',
                                    client_secret='secret',
                                    database='db')
        self.client.session = mock.Mock()
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
        self.datapoint = {
            't': '2014-01-03T00:01:02.123Z',
            'v': 100
        }

    def test_init_minimal(self):
        client = dotide.Client()
        self.assertIsNone(client.client_id)
        self.assertIsNone(client.client_secret)
        self.assertIsNone(client.access_token)
        self.assertIsNone(client.database)
        self.assertIsNotNone(client.access_tokens)

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
        self.assertIsNotNone(client.access_tokens)

    def test_list_access_tokens(self):
        self.client.session.request.return_value = mock_response(
            200, json.dumps([self.access_token]))
        access_tokens = self.client.list_access_tokens()
        self.assertEqual(access_tokens, [self.access_token])

    def test_create_access_token(self):
        self.client.session.request.return_value = mock_response(
            201, json.dumps(self.access_token))
        access_token = self.client.create_access_token(
            data=json.dumps(self.access_token))
        self.assertEqual(access_token, self.access_token)

    def test_read_access_token(self):
        self.client.session.request.return_value = mock_response(
            200, json.dumps(self.access_token))
        access_token = self.client.read_access_token(
            self.access_token['access_token'])
        self.assertEqual(access_token, self.access_token)

    def test_update_access_token(self):
        self.client.session.request.return_value = mock_response(
            200, json.dumps(self.access_token))
        access_token = self.client.update_access_token(
            self.access_token['access_token'],
            data=json.dumps(self.access_token))
        self.assertEqual(access_token, self.access_token)

    def test_delete_access_token(self):
        self.client.session.request.return_value = mock_response(204)
        ret = self.client.delete_access_token(
            self.access_token['access_token'])
        self.assertIsNone(ret)

    def test_list_datastreams(self):
        self.client.session.request.return_value = mock_response(
            200, json.dumps([self.datastream]))
        datastreams = self.client.list_datastreams()
        self.assertEqual(datastreams, [self.datastream])

    def test_create_datastream(self):
        self.client.session.request.return_value = mock_response(
            201, json.dumps(self.datastream))
        datastream = self.client.create_datastream(
            data=json.dumps(self.datastream))
        self.assertEqual(datastream, self.datastream)

    def test_read_datastream(self):
        self.client.session.request.return_value = mock_response(
            200, json.dumps(self.datastream))
        datastream = self.client.read_datastream(self.datastream['id'])
        self.assertEqual(datastream, self.datastream)

    def test_update_datastream(self):
        self.client.session.request.return_value = mock_response(
            200, json.dumps(self.datastream))
        datastream = self.client.update_datastream(
            self.datastream['id'], data=json.dumps(self.datastream))
        self.assertEqual(datastream, self.datastream)

    def test_delete_datastream(self):
        self.client.session.request.return_value = mock_response(204)
        ret = self.client.delete_datastream(self.datastream['id'])
        self.assertIsNone(ret)

    def test_list_datapoint(self):
        self.client.session.request.return_value = mock_response(
            200, json.dumps({'id': self.datastream['id'],
                             'datapoints': [self.datapoint]}))
        ret = self.client.list_datapoints(self.datastream['id'])
        self.assertEqual(ret['id'], self.datastream['id'])
        self.assertEqual(ret['datapoints'][0], self.datapoint)

    def test_create_datapoint(self):
        self.client.session.request.return_value = mock_response(
            201, json.dumps(self.datapoint))
        datapoint = self.client.create_datapoint(
            self.datastream['id'], data=json.dumps(self.datapoint))
        self.assertEqual(datapoint, self.datapoint)

    def test_read_datapoint(self):
        self.client.session.request.return_value = mock_response(
            200, json.dumps(self.datapoint))
        datapoint = self.client.read_datapoint(self.datastream['id'],
                                               self.datapoint['t'])
        self.assertEqual(datapoint, self.datapoint)

    def test_delete_datapoints(self):
        self.client.session.request.return_value = mock_response(204)
        ret = self.client.delete_datapoints(self.datastream['id'],
                                            start=self.datapoint['t'],
                                            end=self.datapoint['t'])
        self.assertIsNone(ret)

    def test_delete_datapoint(self):
        self.client.session.request.return_value = mock_response(204)
        ret = self.client.delete_datapoint(self.datastream['id'],
                                           self.datapoint['t'])
        self.assertIsNone(ret)

if __name__ == '__main__':
    unittest.main()
