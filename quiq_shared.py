import base64

def get_headers(identity, secret):
    encodedAuth = base64.b64encode("{}:{}".format(identity, secret))
    return {"Authorization": "Basic {}".format(encodedAuth), "Content-Type": "application/json", "Accept": "application/json"}
