from easycodefpy.easycodefpy import *
from easycodefpy.properties import ServiceType, PATH_CREATE_ACCOUNT
from .helper import *


def test_check_client_info():
    codef = Codef()
    # 샌드박스는 클라이언트 정보가 상수로 입력되어 있다.
    assert codef.check_client_info(ServiceType.SANDBOX)
    assert not codef.check_client_info(ServiceType.DEMO)
    assert not codef.check_client_info(ServiceType.PRODUCT)

    codef.set_client_info('', 'secret')
    codef.set_demo_client_info('id', '')
    assert not codef.check_client_info(ServiceType.DEMO)
    assert not codef.check_client_info(ServiceType.PRODUCT)

    codef.set_client_info('id', 'secret')
    assert codef.check_client_info(ServiceType.PRODUCT)
    codef.set_demo_client_info('id', 'secret')
    assert codef.check_client_info(ServiceType.DEMO)


def test_request_product_by_empty_client_info():
    codef = Codef()

    param = create_param_for_create_cid()
    res = codef.request_product(PATH_CREATE_ACCOUNT, ServiceType.PRODUCT, param)
    res = json.loads(res)
    assert 'CF-00014' == res['result']['code']


def test_request_product_by_sandbox():
    codef = Codef()

    # 퍼블릭키 셋팅 안했을때
    param = create_param_for_create_cid()
    res = codef.request_product(PATH_CREATE_ACCOUNT, ServiceType.SANDBOX, param)
    res = json.loads(res)
    assert 'CF-00015' == res['result']['code']

    codef.public_key = 'public_key'
    # param == None
    res = codef.request_product(PATH_CREATE_ACCOUNT, ServiceType.SANDBOX, None)
    res = json.loads(res)
    assert 'CF-09999' == res['result']['code']

    # 정상 동작
    res = codef.request_product(PATH_CREATE_ACCOUNT, ServiceType.SANDBOX, param)
    exist_cid(json.loads(res))

    # 2way 키워드가 존재할때
    param['is2Way'] = True
    res = codef.request_product(PATH_CREATE_ACCOUNT, ServiceType.SANDBOX, param)
    res = json.loads(res)
    assert 'CF-03004' == res['result']['code']
    del param['is2Way']
    param['twoWayInfo'] = {}
    res = codef.request_product(PATH_CREATE_ACCOUNT, ServiceType.SANDBOX, param)
    res = json.loads(res)
    assert 'CF-03004' == res['result']['code']


def test_request_certification_invalid_2way():
    codef = Codef()
    codef.public_key = 'public_key'

    def assert_invalid_two_way(data: dict):
        res = codef.request_certification(PATH_CREATE_ACCOUNT, ServiceType.SANDBOX, data)
        res = json.loads(res)
        assert 'CF-03003' == res['result']['code']

    param = create_param_for_create_cid()
    assert_invalid_two_way(param)

    param['is2Way'] = True
    assert_invalid_two_way(param)

    param['twoWayInfo'] = {}
    assert_invalid_two_way(param)

    param['twoWayInfo'] = {
        'jobIndex': 1,
        'threadIndex': 1,
        'jti': '0001',
        'twoWayTimestamp': '012012',
    }
    succ_res = codef.request_certification(PATH_CREATE_ACCOUNT, ServiceType.SANDBOX, param)
    succ_res = json.loads(succ_res)
    assert exist_cid(succ_res)


def test_request_token():
    codef = Codef()
    service_type = ServiceType.SANDBOX
    # 발급 받은 토큰은 자동 셋팅된다
    token = codef.request_token(service_type)
    assert codef.get_access_token(service_type) == token

    # 아직 유요한 토큰이라면 보유하고 있는 토큰을 반환한다
    new_token = codef.request_token(service_type)
    assert token == new_token

    # 만료된 토큰이라면 새로운 토큰을 발급받는다
    expired_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXJ2aWNlX3R5cGUiOiIyIiwic2NvcGUiOlsicmVhZCJdLCJzZXJ2aWNlX25vIjoiMDAwMDAwMDAwMDAwIiwiZXhwIjoxNjAxNDQ0OTc5LCJhdXRob3JpdGllcyI6WyJSRUxBWSJdLCJqdGkiOiI4NjRhMDcwOS1jNTM2LTQyZTQtOTg0Ni0wMmZlZTk4NTE5OWYiLCJjbGllbnRfaWQiOiI1MDM4YTYzNS00ZjJkLTQ2MDUtOTI1ZS0wMTk5MDM1MTIyYjgifQ.QdviRdu0gBOYHhVlX-X0CE20lfrfVWC-teZlIYKPMqh-TL5odP8WjSSwEkK8SupFmo7BpgSZEVaYPvzY5R6700RKODHBQm-zZuxDNMn4xEGhOvw9IBo8aJerpfas0dxD5HeauNf_nE0wt3MrHNfu1g0FCWyOBTcdeGa3LGc5StP42r--DIShrhV1EyWGqOmTHL-Bl6VdedV59-_yLeD-pxFd0tpF5pwuFBaB_KHt5wGpjkWcRbYGW1dV-_0cwmKbf1Afq2iO633QEibBIA22cIndCTL1zq2qgeS71cINOb0ZTX4-bS5mpUfpkYtvLGLG-f51d_nTzdMz2LR7ojIuXw'
    codef.set_access_token(expired_token, service_type)
    new_token = codef.request_token(service_type)
    assert expired_token != new_token
    assert expired_token != codef.get_access_token(service_type)
