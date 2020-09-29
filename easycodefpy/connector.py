import requests
import base64
from typing import Union
from .properties import OAUTH_DOMAIN, PATH_GET_TOKEN, ServiceType
from .message import *
from .easycodefpy import Codef


def request_token(client_id: str, client_secret: str) -> Union[dict, None]:
    """
    액세스 토큰 요청
    :param client_id: 클라이언트 아이디
    :param client_secret: 클라이언트 시크릿
    :return: 토큰을 포함한 객체를 반환한다. 응답 코드 200이 아닐 경우 None을 반환한다.
    """
    url = OAUTH_DOMAIN + PATH_GET_TOKEN
    client_info = '{}:{}'.format(client_id, client_secret)
    b64_auth = base64.b64encode(client_info.encode('utf-8')).decode('utf-8')
    body = 'grant_type=client_credentials&scope=read'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + b64_auth
    }
    with requests.post(url, data=body, headers=headers) as res:
        if res.status_code != requests.codes.ok:
            return None
        return res.json()


def request_product(url: str, token: str, body_str: str) -> dict:
    headers = {
        'Accept': 'application/json',
    }
    if token != '' and token is not None:
        headers['Authorization'] = 'Bearer ' + token
    with requests.post(url, data=body_str, headers=headers) as res:
        s_code = res.status_code
        codes = requests.codes
        if s_code == codes.ok:
            return res.json()
        elif s_code == codes.bad:
            return MESSAGE_BAD_REQUEST
        elif s_code == codes.unauthorized:
            return MESSAGE_UNAUTHORIZED
        elif s_code == codes.forbidden:
            return MESSAGE_FORBIDDEN
        elif s_code == codes.not_found:
            return MESSAGE_NOT_FOUND
        else:
            return MESSAGE_SERVER_ERROR


def set_token(
        client_id: str,
        client_secret: str,
        codef: Codef,
        service_type: ServiceType
):
    """
    코드에프 인스턴스에 액세스 토큰을 셋팅해준다.
    최대 3회까지 시도한다.
    :param client_id:
    :param client_secret:
    :param codef:
    :param service_type:
    :return:
    """
    repeat_cnt = 3
    i = 0
    if codef.get_access_token(service_type) == '':
        while i < repeat_cnt:
            token_dict = request_token(client_id, client_secret)
            if token_dict is None:
                i += 1
                continue
            token = token_dict['access_token']
            if token is not None and token != '':
                codef.set_access_token(token, service_type)
                break
            i += 1
