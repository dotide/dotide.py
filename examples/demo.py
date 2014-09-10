#!/usr/bin/env python

import dotide
from datetime import datetime

CLIENT_ID = ''
CLIENT_SECRET = ''
DB = ''

client = dotide.Dotide(DB,
                       client_id=CLIENT_ID,
                       client_secret=CLIENT_SECRET)

# Create datastream
client.datastreams.create({'id': 'id0',
                           'name': 'name0',
                           'tags': ['tag0'],
                           'properties': {'prop0': 1}
                           })

# List datastreams
client.datastreams.filter({'ids': ['id0', 'id1'],
                         'tags': ['tag0', 'tag1'],
                         'limit': 10,
                         'offset': 0
                         })

# Read datastream
client.datastreams.get('id0')

# Update datstream
client.datastreams.update('id0', {
                          'name': 'name0',
                          'tags': ['tag0'],
                          'properties': {'prop0': 1}
                          })

# Delete datastream
client.datastreams.delete('id0')

# Create datapoints
client.datapoints.create(id='id0',
                         data=[[datetime.utcnow(), 1],
                               [datetime.utcnow(), 2]])

# List datapoints
client.datapoints.filter(id='id0',
                         params={'start': datetime(2014, 1, 1),
                                 'end': datetime.utcnow(),
                                 'order': 'asc',
                                 'limit': 1000,
                                 'offset': 0})

# Read datapoint with exactly timestamp
client.datapoints.get(id='id0',
                      timestamp=datetime(2014, 1, 2, 3, 4, 5, 6000))

# Delete datapoint
client.datapoints.delete(id='id0',
                         params={'start': datetime(2014, 1, 1),
                                 'end': datetime.utcnow()})

# Create access_token
client.access_tokens.create({'scopes': [{
    'permissions': ['read', 'write', 'delete'],
    'global': False,
    'ids': ['id0'],
    'tags': ['tag0']
}]})

# List access_token
access_tokens = client.access_tokens.filter({'limit': 10, 'offset': 0})

# Read access_token
client.access_tokens.get(
    '61e13e47ed0b1b6f6a0ebe598d5ddba0c386a0d856487ec84e973d06b1848221')

# Update access_token
client.access_tokens.update('61e13e47ed0b1b6f6a0ebe598d5ddba0c386a0d856\
                            487ec84e973d06b1848221',
                            {'scopes': [
                                {'permissions': ['read', 'write', 'delete'],
                                 'global': True}
                            ]})

# Delete access_token directly
client.access_tokens.delete('61e13e47ed0b1b6f6a0ebe598d5ddba0c386a0d856\
    487ec84e973d06b1848221')
