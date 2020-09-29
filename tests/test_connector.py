from easycodefpy.connector import *
from easycodefpy.properties import SANDBOX_CLIENT_ID, SANDBOX_CLIENT_SECRET


def test_request_token():
    res = request_token(SANDBOX_CLIENT_ID, SANDBOX_CLIENT_SECRET)
    assert res is not None
    token = res['access_token']
    assert token is not None and token != ''
