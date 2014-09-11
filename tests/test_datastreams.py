import unittest
import mock
import json
from dotide import Dotide
from .helper import mock_response


class TestDatastreams(unittest.TestCase):

    """Tests for datastreams."""

    def setUp(self):
        self.client = Dotide(database='db',
                             client_id='id',
                             client_secret='secret')
        self.client.client.session = mock.Mock()
        self.datastream = {
            'id': '51e51544fa36a48592000074',
            'name': 'Demo Datastream',
            'tags': ['a', 'b', 'c'],
            'properties': {
                'prop0': 'value0'
            },
            'current_t': '2014-01-03T00:01:02.123Z',
            'current_v': 100,
            'created_at': '2014-01-03T00:00:00.001Z',
            'updated_at': '2014-01-03T00:01:02.456Z'
        }

    def test_filter(self):
        self.client.client.session.request.return_value = mock_response(
            200, json.dumps([self.datastream]))
        datastreams = self.client.datastreams.filter()
        self.assertEqual(datastreams, [self.datastream])

    def test_create(self):
        self.client.client.session.request.return_value = mock_response(
            201, json.dumps(self.datastream))
        datastream = self.client.datastreams.create(self.datastream)
        self.assertEqual(datastream, self.datastream)

    def test_get(self):
        self.client.client.session.request.return_value = mock_response(
            200, json.dumps(self.datastream))
        datastream = self.client.datastreams.get(self.datastream['id'])
        self.assertEqual(datastream, self.datastream)

    def test_update(self):
        self.client.client.session.request.return_value = mock_response(
            200, json.dumps(self.datastream))
        datastream = self.client.datastreams.update(self.datastream['id'],
                                                    self.datastream)
        self.assertEqual(datastream, self.datastream)

    def test_delete(self):
        self.client.client.session.request.return_value = mock_response(204)
        ret = self.client.datastreams.delete(self.datastream['id'])
        self.assertEqual(True, ret)


if __name__ == '__main__':
    unittest.main()
