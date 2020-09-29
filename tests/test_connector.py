import json
from .helper import *
from easycodefpy.connector import *
from easycodefpy.properties import\
    SANDBOX_CLIENT_ID,\
    SANDBOX_CLIENT_SECRET,\
    SANDBOX_DOMAIN,\
    PATH_CREATE_ACCOUNT


def test_request_token():
    res = request_token(SANDBOX_CLIENT_ID, SANDBOX_CLIENT_SECRET)
    assert res is not None
    token = res['access_token']
    assert token is not None and token != ''


def exist_cid(data: dict) -> bool:
    code = data['result']['code']
    if code == 'CF-00000':
        cid = data['data']['connectedId']
        if cid is not None and cid != '':
            return True
    else:
        return False


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
