import os
from os import path
from easycodefpy.util import encode_to_file_string, encrypt_rsa


def test_encode_to_file_string():
    real_path = path.dirname(path.realpath(__file__))
    mock = path.join(real_path, 'mock_for_encode.txt')
    with open(mock, 'w') as f:
        f.write('hello world')

    encoded_file = encode_to_file_string(mock)

    expected = 'aGVsbG8gd29ybGQ='
    assert expected == encoded_file
    os.remove(mock)


def test_encrypt_rsa():
    public_key = 'MIIBIjANBgkqhkiG9w0BAQ' + \
    'EFAAOCAQ8AMIIBCgKCAQEAuhRrVDeMf' + \
    'b2fBaf8WmtGcQ23Cie+qDQqnkKG9eZV' + \
    'yJdEvP1rLca+0CUOuAnpE8yGPY3HEbd' + \
    'xKTsbIxxV9H8DCEMntXq2VP4loQoYUl' + \
    '0h9dTjtBVWvhYev0s7N5B8Qu9LtykE2' + \
    'k9KBuSZ+5dXulnHYdYjBaifZL6pzoD1' + \
    'ckXoa4TtIuPjZZGXzr3Ivt5LDxPoPfw' + \
    '1qMdqWRF9/YQSK1jZYa7PNR1Hbd8KB8' + \
    '85VEcXNRU7ADHSgdYRBYB8apsPwaChy' + \
    'jgrV98ATLOD7Dl4RlPtXcx/vEKjVMdt' + \
    'CqJ2IHKeJoUCzBPY59U/mtIhjPuQmwS' + \
    'MLEnLisDWEZMkenO0xJbwOwIDAQAB'

    encrypted = encrypt_rsa('hello world', public_key)
    assert encrypted is not None and encrypted != ''
