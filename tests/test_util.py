import os
import base64
import json
from os import path
from easycodefpy.util import *


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


def test_check_validity():
    expired_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXJ2aWNlX3R5cGUiOiIyIiwic2NvcGUiOlsicmVhZCJdLCJzZXJ2aWNlX25vIjoiMDAwMDAwMDAwMDAwIiwiZXhwIjoxNjAxNDQ0OTc5LCJhdXRob3JpdGllcyI6WyJSRUxBWSJdLCJqdGkiOiI4NjRhMDcwOS1jNTM2LTQyZTQtOTg0Ni0wMmZlZTk4NTE5OWYiLCJjbGllbnRfaWQiOiI1MDM4YTYzNS00ZjJkLTQ2MDUtOTI1ZS0wMTk5MDM1MTIyYjgifQ.QdviRdu0gBOYHhVlX-X0CE20lfrfVWC-teZlIYKPMqh-TL5odP8WjSSwEkK8SupFmo7BpgSZEVaYPvzY5R6700RKODHBQm-zZuxDNMn4xEGhOvw9IBo8aJerpfas0dxD5HeauNf_nE0wt3MrHNfu1g0FCWyOBTcdeGa3LGc5StP42r--DIShrhV1EyWGqOmTHL-Bl6VdedV59-_yLeD-pxFd0tpF5pwuFBaB_KHt5wGpjkWcRbYGW1dV-_0cwmKbf1Afq2iO633QEibBIA22cIndCTL1zq2qgeS71cINOb0ZTX4-bS5mpUfpkYtvLGLG-f51d_nTzdMz2LR7ojIuXw'
    base64_str = expired_token.split('.')[1]
    decoded_bytes = base64.b64decode(base64_str + ('=' * (-len(base64_str) % 4)))
    dict_str = decoded_bytes.decode('utf-8')
    data = json.loads(dict_str)
    assert not check_validity(data['exp'])
