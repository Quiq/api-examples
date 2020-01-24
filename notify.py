#!/usr/bin/env python

import argparse
import json
import requests
from quiq_shared import get_headers

parser = argparse.ArgumentParser(description='Sends a message to the specified phone number')
parser.add_argument('-c', '--contactpoint', required=True, help='The contact point to send from')
parser.add_argument('-t', '--topic', required=True, help='The outbound topic to send on')
parser.add_argument('-n', '--handle', required=True, help='The customer handle (i.e. phone number +1-XXX-XXX-XXXX) to send to.')
parser.add_argument('-u', '--identity', required=True, help='The app token identity.')
parser.add_argument('-s', '--secret', required=True, help='The app token secret.')
parser.add_argument('-d', '--domain', required=True, help='The Quiq domain. i.e. company.goquiq.com')

args = parser.parse_args()

payload = {
    'topic': args.topic,
    'contactPoint': args.contactpoint,
    'notifications': [
        {
            'precedence': [],
            'searchInfo': {
                'phoneNumber': args.handle
            },
            'messageMap': {
                'default': {'text': 'This is an outbound notification sent through Quiq'},
            }
        }
    ]
}

print("POSTING payload of: {}".format(payload))

headers = get_headers(args.identity,args.secret)
res = requests.post('https://{}/api/v1/messaging/notify'.format(args.domain, args.platform), data=json.dumps(payload), headers=headers)

print("Status Code: {}".format(res.status_code))
print("Response: {}".format(res.json()))
