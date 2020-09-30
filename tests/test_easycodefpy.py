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


def test_is_empty_two_way_keyword():
    data = {
        'is2Way': True,
        'twoWayInfo': 'info',
    }
    assert not is_empty_two_way_keyword(data)
    del data['is2Way']
    assert not is_empty_two_way_keyword(data)
    del data['twoWayInfo']
    assert is_empty_two_way_keyword(data)


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
