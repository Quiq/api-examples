#!/usr/bin/env python

import argparse
import json
import requests
from quiq_shared import get_headers

parser = argparse.ArgumentParser(description='Sends a message to the specified phone number')
parser.add_argument('-c', '--contactpoint', required=True, help='The contact point to send from')
parser.add_argument('-p', '--platform', required=True, help='The platform to send from. Only SMS is supported currently.')
parser.add_argument('-n', '--handle', required=True, help='The customer handle (i.e. phone number +1-XXX-XXX-XXXX) to send to.')
parser.add_argument('-u', '--identity', required=True, help='The app token identity.')
parser.add_argument('-s', '--secret', required=True, help='The app token secret.')
parser.add_argument('-d', '--domain', required=True, help='The Quiq domain. i.e. company.goquiq.com')

args = parser.parse_args()

domain = args.domain
contact_point = args.contactpoint
identity = args.identity
secret = args.secret
platform = args.platform
cust_handle = args.handle

payload = {
    'handle': cust_handle,
    'contactPoint': contact_point,
    'message' : {
        'text': 'Message text to be sent via SMS'
    }
}

print "POSTING payload of: {}".format(payload)

headers = get_headers(identity,secret)

# This API sends a single message to a single number. Quiq will not create a conversation
# until the end user responds.
res = requests.post('https://{}/api/v1/messaging/platforms/{}/send-notification'.format(domain, platform), data=json.dumps(payload), headers=headers)

print "Status Code: {}".format(res.status_code)
print "Response: {}".format(res.json())
