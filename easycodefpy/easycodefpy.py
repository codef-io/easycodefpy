class AccessToken(object):

    def __init__(self):
        self.product = ''
        self.demo = ''
        self.sandbox = ''


class Codef(object):

    def __init__(self):
        self.access_token = AccessToken()
        self.demo_client_id = ''
        self.demo_client_secret = ''
        self.client_id = ''
        self.client_secret = ''
        self.public_key = ''
