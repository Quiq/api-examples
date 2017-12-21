#!/usr/bin/env python

import argparse
import json
import requests
from quiq_shared import get_headers

parser = argparse.ArgumentParser(description='A script that takes a .csv of customer handles and messages and executes a bulk notification request against Quiq.')
parser.add_argument('-i', '--inputfile', required=True, help='Input file in expected CSV format of customerHandle, messageText')
parser.add_argument('-c', '--contactpoint', required=True, help='The contact point to send from')
parser.add_argument('-p', '--platform', required=True, help='The platform to send from. Only SMS is supported currently.')
parser.add_argument('-u', '--identity', required=True, help='The app token identity.')
parser.add_argument('-s', '--secret', required=True, help='The app token secret.')
parser.add_argument('-d', '--domain', required=True, help='The Quiq domain. i.e. company.goquiq.com')

args = parser.parse_args()

domain = args.domain
contact_point = args.contactpoint
identity = args.identity
secret = args.secret
platform = args.platform
file = open(args.inputfile)

notifications = []
for line in file:
    customerHandle, messageText = line.split(",")
    notifications.append({"handle": customerHandle, "message": {"text": messageText.strip()}})

payload = json.dumps({"contactPoint": contact_point, "notifications": notifications})

print "POSTING payload of: {}".format(payload)

headers = get_headers(identity,secret)
res = requests.post('https://{}/api/v1/messaging/platforms/{}/send-notifications'.format(domain, platform), data=payload, headers=headers)

print "Status Code: {}".format(res.status_code)
print "Response: {}".format(res.json())
