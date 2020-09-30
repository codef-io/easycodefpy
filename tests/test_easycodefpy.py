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


