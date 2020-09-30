from easycodefpy.util import encrypt_rsa


def create_param_for_create_cid() -> dict:
	public_key = 'MIIBIjANBgkqhkiG9w0BAQ' +\
		'EFAAOCAQ8AMIIBCgKCAQEAuhRrVDeMf' +\
		'b2fBaf8WmtGcQ23Cie+qDQqnkKG9eZV' +\
		'yJdEvP1rLca+0CUOuAnpE8yGPY3HEbd' +\
		'xKTsbIxxV9H8DCEMntXq2VP4loQoYUl' +\
		'0h9dTjtBVWvhYev0s7N5B8Qu9LtykE2' +\
		'k9KBuSZ+5dXulnHYdYjBaifZL6pzoD1' +\
		'ckXoa4TtIuPjZZGXzr3Ivt5LDxPoPfw' +\
		'1qMdqWRF9/YQSK1jZYa7PNR1Hbd8KB8' +\
		'85VEcXNRU7ADHSgdYRBYB8apsPwaChy' +\
		'jgrV98ATLOD7Dl4RlPtXcx/vEKjVMdt' +\
		'CqJ2IHKeJoUCzBPY59U/mtIhjPuQmwS' +\
		'MLEnLisDWEZMkenO0xJbwOwIDAQAB'
	password = encrypt_rsa('password', public_key)
	return {
		'accountList': [{
			'countryCode': 'KR',
			'businessType': 'BK',
			'clientType': 'P',
			'organization': '0004',
			'loginType': '1',
			'id': 'testID',
			'password': password,
		}],
	}


def exist_cid(data: dict) -> bool:
	code = data['result']['code']
	if code == 'CF-00000':
		cid = data['data']['connectedId']
		if cid is not None and cid != '':
			return True
	else:
		return False
