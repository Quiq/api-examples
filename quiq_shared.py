import base64

# Returns the HTTP headers needed to connect to the Quiq API.
# The identity and secret are not your Quiq username and password. They are individual API keys.
def get_headers(identity, secret):

    # Encode this string using Base 64
    encodedAuth = base64.b64encode("{}:{}".format(identity, secret))

    # In addition to the authentication, set the content type to JSON using the HTTP headers
    return {"Authorization": "Basic {}".format(encodedAuth), "Content-Type": "application/json", "Accept": "application/json"}
