from easycodefpy.properties import *


def test_get_codef_domain():
    assert API_DOMAIN == get_codef_domain(ServiceType.PRODUCT)
    assert DEMO_DOMAIN == get_codef_domain(ServiceType.DEMO)
    assert SANDBOX_DOMAIN == get_codef_domain(ServiceType.SANDBOX)
