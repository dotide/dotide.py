#!/usr/bin/env python

import dotide
from datetime import datetime

CLIENT_ID = ''
CLIENT_SECRET = ''
DB = ''

client = dotide.Client(client_id=CLIENT_ID,
                       client_secret=CLIENT_SECRET,
                       databaseb=DB)

# List datastreams
datastreams = client.datastreams.filter(ids=['id0', 'id1'],
                                        tags='tag0,tag1',
                                        limit=10,
                                        offset=10
                                        )

# Read datastream
datastream = client.datastreams.get('id0')
print datastream.type

# Create datastream
datastream = client.datastreams.create(id='id0',
                                       name='name0',
                                       type='number',
                                       tags=['tag0'],
                                       proerties={'prop0': 1}
                                       )

# Update datstream
datastream.tags.append('tag1')
datastream.save()

# Delete datastream
datastream.delete()

# List datapoints
datapoints = datastream.datapoints.filter(start=datetime(2014, 1, 1),
                                          end=datetime.now(),
                                          order='asc',
                                          limit=1000)

# Create datapoints
datapoint = datastream.datapoints.create(t=datetime.now(), v=1)
datapoints = datastream.datapoints.create([{'t': datetime.now(), 'v': 1},
                                           {'t': datetime.now(), 'v': 2}]
                                          )

# Read datapoint with exactly timestamp
datapoint = datastream.datapoints.get(datetime(2014, 1, 2, 3, 4, 5, 6000))

# Delete datapoint
datastream.datapoints.delete(start=datetime(2014, 1, 1),
                             end=datetime.now())
