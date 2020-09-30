import base64
import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1


def encode_to_file_string(file_path: str) -> str:
    """
    파일을 base64 문자열로 인코딩한다.
    :
    :param file_path: 파일 경로
    :return: 인코딩된 file string
    """
    fp = open(file_path, 'rb')
    data = fp.read()
    fp.close()
    return base64.b64encode(data).decode('utf-8')


def encrypt_rsa(text: str, public_key: str) -> str:
    """
     RSA 암호화
    :param text: 암호화할 데이터
    :param public_key: CODEF 회원에게 제공되는 PublicKey
    :return: RSA256 암호화된 데이터
    """
    key_der = base64.b64decode(public_key)
    key_pub = RSA.importKey(key_der)
    cipher = PKCS1.new(key_pub)
    cipher_text = cipher.encrypt(text.encode())

    return base64.b64encode(cipher_text).decode('utf-8')


def check_validity(exp: int) -> bool:
    """
    토큰 정합성 체크를 도와주는 유틸
    :param exp: 토큰 내부 만료 시간
    :return: 유효하다면 True
    """
    now = int(round(time.time() * 1000))
    exp = int(str(exp) + '000')
    if now > exp or (exp - now < (60 * 60 * 1000)):
        return False

    return True
