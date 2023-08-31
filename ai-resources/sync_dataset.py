#!/usr/bin/env python3
import json
import os
import requests
import argparse
import mimetypes

ap = argparse.ArgumentParser()
ap.add_argument('--host')
ap.add_argument('--dataset-id', '-d')
ap.add_argument('file')
args = ap.parse_args()

identity = os.environ['QUIQ_API_KEY_IDENTITY']
secret = os.environ['QUIQ_API_KEY_SECRET']

auth = (identity, secret)

def prepare_upload():
    resp = requests.post(f'{args.host}/api/v1/assets/uploads/prepare', json={'numUploads': 1}, auth=auth)
    form_info = resp.json()['uploads'][0]

    upload_id = form_info['uploadId']
    directive = form_info['directive']
    form = {e['name']: e['value'] for e in directive['formEntries']}
    content_type = mimetypes.guess_type(args.file)[0]
    form['Content-Type'] = content_type
    return form, directive['url'], upload_id

def upload(form, url, filepath):
    resp = requests.post(url, data=form, files={'file': open(filepath, 'rb')})
    return resp

form, url, upload_id = prepare_upload()
print(f"Prepared upload {upload_id}")
resp = upload(form, url, args.file)
print(f"Uploaded {args.file}: {resp.status_code} {resp.text}")

payload = {
    'syncUploadId': upload_id,
}

resp = requests.post(f"{args.host}/api/v1/ai-resources/dataset/{args.dataset_id}/sync", json=payload, auth=auth)

print(f"Syncing dataset {args.dataset_id}")
print(resp.status_code, resp.text)

