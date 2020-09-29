import requests
import base64
from typing import Union
from .properties import OAUTH_DOMAIN, PATH_GET_TOKEN
from .message import *


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

