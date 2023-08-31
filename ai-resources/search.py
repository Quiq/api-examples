#!/usr/bin/env python3
import json
import os
import requests
import argparse
import mimetypes

ap = argparse.ArgumentParser()
ap.add_argument('--host')
ap.add_argument('--index-id', '-i')
ap.add_argument('--search-text', '-t')
args = ap.parse_args()

identity = os.environ['QUIQ_API_KEY_IDENTITY']
secret = os.environ['QUIQ_API_KEY_SECRET']

auth = (identity, secret)

payload = {
    'searchIndexId': args.index_id,
    'searchText': args.search_text,
    'topK': 5
}

resp = requests.post(f"{args.host}/api/v1/ai-resources/search", json=payload, auth=auth).json()

for result in resp['results']:
    print(result)

