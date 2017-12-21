import base64

# Gets the HTTP headers needed to connect to the Quiq API.
# The identity and secret are not your Quiq username and password. They are individual API keys.
def get_headers(identity, secret):
    encodedAuth = base64.b64encode("{}:{}".format(identity, secret))
    return {"Authorization": "Basic {}".format(encodedAuth), "Content-Type": "application/json", "Accept": "application/json"}
