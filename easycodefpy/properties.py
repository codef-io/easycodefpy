from enum import Enum

OAUTH_DOMAIN = 'https://oauth.codef.io'
DEMO_DOMAIN = 'https://development.codef.io'
API_DOMAIN = 'https://api.codef.io'
SANDBOX_DOMAIN = 'https://sandbox.codef.io'

PATH_GET_TOKEN = '/oauth/token'
PATH_CREATE_ACCOUNT = '/v1/account/create'
PATH_ADD_ACCOUNT = '/v1/account/add'
PATH_UPDATE_ACCOUNT = '/v1/account/update'
PATH_DELETE_ACCOUNT = '/v1/account/delete'
PATH_GET_ACCOUNT_LIST = '/v1/account/list'
PATH_GET_CID_LIST = '/v1/account/connectedId-list'

SANDBOX_CLIENT_ID = 'ef27cfaa-10c1-4470-adac-60ba476273f9'
SANDBOX_CLIENT_SECRET = '83160c33-9045-4915-86d8-809473cdf5c3'

KEY_RESULT = 'result'
KEY_CODE = 'code'
KEY_MESSAGE = 'message'
KEY_EXTRA_MESSAGE = 'extraMessage'
KEY_DATA = 'data'
KEY_ACCOUNT_LIST = 'accountList'
KEY_CONNECTED_ID = 'connectedId'
KEY_INVALID_TOKEN = 'invalidToken'
KEY_ACCESS_DENIED = 'accessDenied'


class ServiceType(Enum):
    PRODUCT = 0
    DEMO = 1
    SANDBOX = 2


def get_codef_domain(service_type: ServiceType) -> str:
    if service_type == ServiceType.PRODUCT:
        return API_DOMAIN
    elif service_type == ServiceType.DEMO:
        return DEMO_DOMAIN
    else:
        return SANDBOX_DOMAIN
