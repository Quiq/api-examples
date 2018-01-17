#!/usr/bin/env python

import requests
import json
import argparse
from quiq_shared import get_headers

'''
Example script to demonstrate the Quiq Start Conversation API.
Optional RightNow integration referneces can be used with this script.
'''

parser = argparse.ArgumentParser(description='Example script to demonstrate the Quiq Start Conversation API.')
parser.add_argument('-c', '--contactpoint', required=True, help='The contact point to send from.')
parser.add_argument('-n', '--handle', required=True, help='The customer handle (i.e. phone number +1-XXX-XXX-XXXX) to send to.')
parser.add_argument('-p', '--platform', required=True, help='The platform to send from. Only SMS is supported currently.')
parser.add_argument('-u', '--identity', required=True, help='The app token identity.')
parser.add_argument('-s', '--secret', required=True, help='The app token secret.')
parser.add_argument('-d', '--domain', required=True, help='The Quiq domain. i.e. company.goquiq.com')
parser.add_argument('-i', '--incident', required=False, help='The RightNow incident ID you wish to associate this conversation with.')
parser.add_argument('-r', '--refno', required=False, help='The RightNow refernce number you wish to associate this conversation with.')

args = parser.parse_args()

start_conversation_url = 'https://{args.domain}.goquiq.com/api/v1/messaging/platforms/{args.platform}/start-conversation'.format(**vars())

start_conversation_payload = {
  'handle': args.handle,
  'contactPoint': args.contactpoint,
  'messages': [
    {
      'text': 'Testing the start convo API using the example Python script',
      'authorType': 'System',
      'imported': False
    }
  ],
  'integrations': [
    {
      'provider': 'rightnow',
      'name': 'incident',
      'id': args.incident
    },
    {
      'provider': 'rightnow',
      'name': 'refno',
      'id': args.refno
    }
  ] if args.incident is not None and args.refno is not None else [],
  'integrationsData': {}
}

print "POSTING payload of: {}".format(start_conversation_payload)

headers = get_headers(args.identity,args.secret)
res = requests.post(start_conversation_url, data=json.dumps(start_conversation_payload), headers=headers)

print "Status Code: {}".format(res.status_code)
print "Response: {}".format(res.json())
