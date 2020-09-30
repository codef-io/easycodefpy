from .helper import *
from easycodefpy.connector import *
from easycodefpy.properties import\
    SANDBOX_CLIENT_ID,\
    SANDBOX_CLIENT_SECRET,\
    SANDBOX_DOMAIN,\
    PATH_CREATE_ACCOUNT
from easycodefpy.easycodefpy import Codef


def test_request_token():
    res = request_token(SANDBOX_CLIENT_ID, SANDBOX_CLIENT_SECRET)
    assert res is not None
    token = res['access_token']
    assert token is not None and token != ''


def test_request_product():
    param = create_param_for_create_cid()
    access_token = ''
    # test for 404 error
    res = request_product(SANDBOX_DOMAIN + "/failPath", access_token, json.dumps(param))
    assert 'CF-00404' == res['result']['code']

    # test for success
    token_dict = request_token(SANDBOX_CLIENT_ID, SANDBOX_CLIENT_SECRET)
    access_token = token_dict['access_token']
    res = request_product(SANDBOX_DOMAIN + PATH_CREATE_ACCOUNT, access_token, json.dumps(param))
    assert exist_cid(res)


def test_set_token():
    codef = Codef()
    set_token(SANDBOX_CLIENT_ID, SANDBOX_CLIENT_SECRET, codef, ServiceType.SANDBOX)
    token = codef.get_access_token(ServiceType.SANDBOX)
    assert token != ''


def test_excute():
    codef = Codef()
    param = create_param_for_create_cid()
    res = execute(PATH_CREATE_ACCOUNT, param, codef, ServiceType.SANDBOX)
    assert res is not None
    assert exist_cid(res)

# def test_fail_set_token_must_unauth():
#     codef = Codef()
#     codef.public_key = 'public_key'
#     codef.set_client_info('id', 'secret')
#
#     param = {
#         'connectedId': '8PQI4dQ......hKLhTnZ',
#         'organization': '0004',
#         'identity': '1130000627',
#     }
#     product_url = '/v1/kr/card/b/account/card-list'


