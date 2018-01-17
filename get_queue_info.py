#!/usr/bin/env python

import argparse
import json
import requests
from quiq_shared import get_headers

parser = argparse.ArgumentParser(description='Gets the estimated wait time in milliseconds for the specified queue')
parser.add_argument('-u', '--identity', required=True, help='The app token identity.')
parser.add_argument('-s', '--secret', required=True, help='The app token secret.')
parser.add_argument('-d', '--domain', required=True, help='The Quiq domain. i.e. company.goquiq.com')
parser.add_argument('-q', '--queue', required=True, help='The Quiq queue name')

args = parser.parse_args()

headers = get_headers(args.identity,args.secret)

print "Retrieving queue info for queue {}".format(args.queue)

url = 'https://{}/api/v1/messaging/queues/{}/info/'.format(args.domain, args.queue)
res = requests.get(url, headers=headers)

print "Status Code: {}".format(res.status_code)
print "Response: {}".format(res.json())
