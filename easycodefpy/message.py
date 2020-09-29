from .properties import\
    KEY_CODE,\
    KEY_MESSAGE,\
    KEY_EXTRA_MESSAGE,\
    KEY_RESULT,\
    KEY_DATA


def create_message(code: str, msg: str) -> dict:
    err_info = {
        KEY_CODE: code,
        KEY_MESSAGE: msg,
        KEY_EXTRA_MESSAGE: ''
    }
    return {
        KEY_RESULT: err_info,
        KEY_DATA: {},
    }


MESSAGE_OK = create_message('CF-00000', '성공')
MESSAGE_INVALID_JSON = create_message('CF-00002', 'json형식이 올바르지 않습니다.')
MESSAGE_INVALID_PARAMETER = create_message('CF-00007', '요청 파라미터가 올바르지 않습니다.')
MESSAGE_UNSUPPORTED_ENCODING = create_message('CF-00009', '지원하지 않는 형식으로 인코딩된 문자열입니다.')
MESSAGE_EMPTY_CLIENT_INFO = create_message('CF-00014', '상품 요청을 위해서는 클라이언트 정보가 필요합니다. 클라이언트 아이디와 시크릿 정보를 설정하세요.')
MESSAGE_EMPTY_PUBLIC_KEY = create_message('CF-00015', '상품 요청을 위해서는 퍼블릭키가 필요합니다. 퍼블릭키 정보를 설정하세요.')
MESSAGE_INVALID_2WAY_INFO = create_message('CF-03003', '2WAY 요청 처리를 위한 정보가 올바르지 않습니다. 응답으로 받은 항목을 그대로 2way요청 항목에 포함해야 합니다.')
MESSAGE_INVALID_2WAY_KEYWORD = create_message('CF-03004', '추가 인증(2Way)을 위한 요청은 requestCertification메서드를 사용해야 합니다.')
MESSAGE_BAD_REQUEST = create_message('CF-00400', '클라이언트 요청 오류로 인해 요청을 처리 할 수 ​​없습니다.')
MESSAGE_UNAUTHORIZED = create_message('CF-00401', '요청 권한이 없습니다.')
MESSAGE_FORBIDDEN = create_message('CF-00403', '잘못된 요청입니다.')
MESSAGE_NOT_FOUND = create_message('CF-00404', '요청하신 페이지(Resource)를 찾을 수 없습니다.')
MESSAGE_METHOD_NOT_ALLOWED = create_message('CF-00405', '요청하신 방법(Method)이 잘못되었습니다.')
MESSAGE_LIBRARY_SENDER_ERROR = create_message('CF-09980', '통신 요청에 실패했습니다. 응답정보를 확인하시고 올바른 요청을 시도하세요.')
MESSAGE_SERVER_ERROR = create_message('CF-09999', '서버 처리중 에러가 발생 했습니다. 관리자에게 문의하세요.')
