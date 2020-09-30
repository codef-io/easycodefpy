import json
import re
from .connector import execute
from .properties import ServiceType, SANDBOX_CLIENT_ID, SANDBOX_CLIENT_SECRET
from .message import\
    MESSAGE_EMPTY_CLIENT_INFO,\
    MESSAGE_EMPTY_PUBLIC_KEY,\
    MESSAGE_INVALID_2WAY_KEYWORD,\
    MESSAGE_INVALID_2WAY_INFO

pattern = re.compile(r'\s+')


def trim_all(sentence: str) -> str:
    return re.sub(pattern, '', sentence)


def _is_empty_two_way_keyword(data: dict) -> bool:
    """
    2way 키워드가 비워져 있는지 확인한다.
    :param data: 파라미터
    :return: 비워져 있을때 True
    """
    if data is None:
        return True

    try:
        _ = data['is2Way']
        return False
    except KeyError:
        pass
    try:
        _ = data['twoWayInfo']
        return False
    except KeyError:
        return True


def _check_need_value_in_two_way_info(two_way_info: dict) -> bool:
    try:
        return two_way_info['jobIndex'] is not None and\
               two_way_info['threadIndex'] is not None and\
               two_way_info['jti'] is not None and\
               two_way_info['twoWayTimestamp'] is not None
    except KeyError:
        return False


def _has_two_way_keyword(data: dict) -> bool:
    try:
        is_2way = data['is2Way']
        if is_2way is None or type(is_2way) != bool:
            return False

        two_way_info = data['twoWayInfo']
        if two_way_info is None or type(two_way_info) != dict:
            return False

        return _check_need_value_in_two_way_info(two_way_info)
    except KeyError:
        return False


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
    """
    CODEF API를 사용하기 위한 유저 제공 클래스다.
    """

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

    def get_client_info(self, service_type: ServiceType) -> (str, str):
        if service_type == ServiceType.PRODUCT:
            return self.client_id, self.client_secret
        elif service_type == ServiceType.DEMO:
            return self.demo_client_id, self.demo_client_secret
        else:
            return SANDBOX_CLIENT_ID, SANDBOX_CLIENT_SECRET

    def set_client_info(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

    def set_demo_client_info(self, client_id: str, client_secret: str):
        self.demo_client_id = client_id
        self.demo_client_secret = client_secret

    def request_product(self, product_path: str, service_type: ServiceType, param: dict) -> str:
        # 클라이언트 정보 체크
        if not self.check_client_info(service_type):
            return json.dumps(MESSAGE_EMPTY_CLIENT_INFO, ensure_ascii=False)

        # 퍼블릭키 정보 체크
        if self.public_key is None or trim_all(self.public_key) == '':
            return json.dumps(MESSAGE_EMPTY_PUBLIC_KEY, ensure_ascii=False)

        # 추가인증 키워드 체크
        if not _is_empty_two_way_keyword(param):
            return json.dumps(MESSAGE_INVALID_2WAY_KEYWORD, ensure_ascii=False)

        res = execute(product_path, param, self, service_type)
        if res is None:
            return ''
        return json.dumps(res, ensure_ascii=False)

    def request_certification(self, product_path: str, service_type: ServiceType, param: dict) -> str:
        # 클라이언트 정보 체크
        if not self.check_client_info(service_type):
            return json.dumps(MESSAGE_EMPTY_CLIENT_INFO, ensure_ascii=False)

        # 퍼블릭키 정보 체크
        if self.public_key is None or trim_all(self.public_key) == '':
            return json.dumps(MESSAGE_EMPTY_PUBLIC_KEY, ensure_ascii=False)

        # 추가인증 파라미터 필수 입력 체크
        if not _has_two_way_keyword(param):
            return json.dumps(MESSAGE_INVALID_2WAY_INFO, ensure_ascii=False)

        res = execute(product_path, param, self, param)
        return json.dumps(res, ensure_ascii=False)

    def check_client_info(self, service_type: ServiceType) -> bool:
        """
        서비스 번호에 해당하는 클라이언트 정보를 체크한다.
        :param service_type: 서비스 타입
        :return: 이상 없다면 True
        """
        if service_type == ServiceType.PRODUCT:
            return not (trim_all(self.client_id) == '' or trim_all(self.client_secret) == '')
        elif service_type == ServiceType.DEMO:
            return not (trim_all(self.demo_client_id) == '' or trim_all(self.demo_client_secret) == '')
        else:
            return not (trim_all(SANDBOX_CLIENT_ID) == '' or trim_all(SANDBOX_CLIENT_SECRET) == '')
