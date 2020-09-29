from .properties import ServiceType


class AccessToken(object):

    def __init__(self):
        self.product = ''
        self.demo = ''
        self.sandbox = ''

    def get_access_token(self, service_type: ServiceType) -> str:
        if service_type == ServiceType.PRODUCT:
            return self.product
        elif service_type == ServiceType.DEMO:
            return self.demo
        else:
            return self.sandbox

    def set_access_token(self, token: str, service_type: ServiceType):
        if service_type == ServiceType.PRODUCT:
            self.product = token
        elif service_type == ServiceType.DEMO:
            self.demo = token
        else:
            self.sandbox = token


class Codef(object):

    def __init__(self):
        self.access_token = AccessToken()
        self.demo_client_id = ''
        self.demo_client_secret = ''
        self.client_id = ''
        self.client_secret = ''
        self.public_key = ''

    def get_access_token(self, service_type: ServiceType) -> str:
        return self.access_token.get_access_token(service_type)

    def set_access_token(self, token: str, service_type: ServiceType):
        self.access_token.set_access_token(token, service_type)

    def set_client_info(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def set_demo_client_info(self, client_id, client_secret):
        self.demo_client_id = client_id
        self.client_secret = client_secret
