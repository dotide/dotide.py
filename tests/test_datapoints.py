import unittest
import mock
import json
from dotide import Dotide
from .helper import mock_response


class TestDatapoints(unittest.TestCase):

    """Tests for datapoints"""

    def setUp(self):
        self.client = Dotide(database='db',
                             client_id='id',
                             client_secret='secret')
        self.client.client.session = mock.Mock()
        self.datapoint = ['2014-01-03T00:01:02.123Z', 100]

    def test_filter(self):
        self.client.client.session.request.return_value = mock_response(
            200, json.dumps([self.datapoint]))
        datapoints = self.client.datapoints.filter(id='id')
        self.assertEqual(datapoints, [self.datapoint])

    def test_create(self):
        self.client.client.session.request.return_value = mock_response(
            201, json.dumps([self.datapoint]))
        datapoint = self.client.datapoints.create('id', [self.datapoint])
        self.assertEqual(datapoint, [self.datapoint])

    def test_get(self):
        self.client.client.session.request.return_value = mock_response(
            200, json.dumps(self.datapoint))
        datapoint = self.client.datapoints.get('id', self.datapoint[0])
        self.assertEqual(datapoint, self.datapoint)

    def test_delete(self):
        self.client.client.session.request.return_value = mock_response(204)
        ret = self.client.datapoints.delete(
            'id', {'start': self.datapoint[0], 'end': self.datapoint[0]})
        self.assertEqual(True, ret)


if __name__ == '__main__':
    unittest.main()
