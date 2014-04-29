#!/usr/bin/env python

import dotide
from datetime import datetime

CLIENT_ID = ''
CLIENT_SECRET = ''
DB = ''

client = dotide.Client(DB,
                       client_id=CLIENT_ID,
                       client_secret=CLIENT_SECRET)

# List datastreams
datastreams = client.datastreams.filter(ids=['id0', 'id1'],
                                        tags=['tag0', 'tag1'],
                                        limit=10,
                                        offset=10
                                        )

# Create datastream
datastream = client.datastreams.create(id='id0',
                                       name='name0',
                                       type='number',
                                       tags=['tag0'],
                                       properties={'prop0': 1}
                                       )

# Read datastream
datastream = client.datastreams.get('id0')

# Update datstream
datastream.tags.append('tag1')
datastream.save()

# Update datastream directly
datastream = client.datastreams.update('id0',
                                       name='name0',
                                       tags=['tag0'],
                                       properties={'prop0': 1}
                                       )

# Delete datastream
datastream.delete()

# Delete datastream directly
client.datastreams.delete('id0')

# List datapoints
datapoints = datastream.datapoints.filter(start=datetime(2014, 1, 1),
                                          end=datetime.utcnow(),
                                          order='asc',
                                          limit=1000)

# Create datapoints
datapoint = datastream.datapoints.create(t=datetime.utcnow(), v=1)
datapoints = datastream.datapoints.create([{'t': datetime.utcnow(), 'v': 1},
                                           {'t': datetime.utcnow(), 'v': 2}]
                                          )

# Read datapoint with exactly timestamp
datapoint = datastream.datapoints.get(datetime(2014, 1, 2, 3, 4, 5, 6000))

# Delete datapoint
datastream.datapoints.delete(datetime(2014, 1, 2, 3, 4, 5, 6000))
datastream.datapoints.delete(start=datetime(2014, 1, 1),
                             end=datetime.utcnow())

# List access_token
access_tokens = client.access_tokens.filter()

# Create access_token
access_token = client.access_tokens.create(scopes=[{
    'permissions': ['read', 'write', 'delete'],
    'global': False,
    'ids': ['id0'],
    'tags': ['tag0']
}])

# Read access_token
access_token = client.access_tokens.get('61e13e47ed0b1b6f6a0ebe598d5ddba0c386a\
                                        0d856487ec84e973d06b1848221')

# Update access_token
access_token = client.access_tokens.get('61e13e47ed0b1b6f6a0ebe598d5ddba0c386a\
                                        0d856487ec84e973d06b1848221')
access_token.scopes = [{'permissions': ['read', 'write', 'delete'],
                       'global': True}]
access_token.save()

# Update access_token directly
access_token = client.access_tokens.update(
    '61e13e47ed0b1b6f6a0ebe598d5ddba0c386a0d856487ec84e973d06b1848221',
    scopes=[{'permissions': ['read', 'write', 'delete'], 'global': True}])

# Delete access_token
access_token = client.access_tokens.get('61e13e47ed0b1b6f6a0ebe598d5ddba0c386a\
                                        0d856487ec84e973d06b1848221')
access_token.delete()

# Delete access_token directly
client.access_tokens.delete('61e13e47ed0b1b6f6a0ebe598d5ddba0c386a0d856487ec84\
                            e973d06b1848221')
