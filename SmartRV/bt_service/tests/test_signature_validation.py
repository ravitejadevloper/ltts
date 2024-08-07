
import os
import sys
import logging
from datetime import datetime
logger = logging.getLogger(__name__)

from fastapi.testclient import TestClient

import pytest


non_mac = pytest.mark.skipif(
    sys.platform.startswith('darwin'),
    reason="DBUS module not available on MAC"
)
in_dev = pytest.mark.skip(
    reason="Refactor needed to pass tests on any platform"
)
# if sys.platform.startswith("darwin"):
#     pytest.skip("skipping windows-only tests", allow_module_level=True)


@non_mac
@pytest.fixture
def client():
    from bt_service.wgo_bt_service import app
    with TestClient(app) as c:
        yield c


@non_mac
@in_dev
def test_signature_validation():
    '''Perform signature validation against the environment public key.'''
    from bt_service.wgo_bt_service import _decode_cert_body

    pub_key_path = '/Users/dom/Documents/1_Projects/1_Winnebago/2_Dev/storage/certs/env_pub.pem'

    data = '0a50026d48286500000000f1e2fcb60a8a1d4a996072633c6e7dc33130353430343252503030312d303030300000000000000010d65a974a21cba6c4121dfbde0213dbf1190ffa96bd57db2bdba4820578521e2f84355ce7359eef77bcbfd8fbff23ca23039353582f7a1284dde2d01e33d1c1aa52a6c9cfa2ac358072242cd7b925142455883ebf967efaf7aa63f5432b38205955693ad3f52b816d3d0ca3a6a2a33fc2227f920a9a6d15e529c62a84e2d4ea72901d6548aca0516ba661a59a4691833710d5094132fea331a103881449d6638a02ebfc665e1509da903cf3369655bca3bb6b16d28b0aba3de1a4507ae036fac42047f1b9048ff47ee7fd8de8ef52dfbf0fa8cace8afc8098554551b4d8939e00bf73a5e1c2f175dbfe18393e3ce74ef12abd3f8598ce1b33f8b7bf3ece37169187967d67e351c3b3d0381885fd1981069a6385ef266d95c159d2d79af4c0162d9d01c833c1d7595b2cd87ab611ebd4b2cc286254f8d3f3f09a618ce7a689f1be0368fa79d9c3a6d0754cc4b58e7fa74efecd29043397f18c4476e4c0e8be69280b5fdd0a9343799762fd5a36db500bcf2237bae5ccd3749955084f2a3f8c5b3ae1adf76ae1fe67c854b10b5b1d418edd15ec49c872599254c111796e03e2ee32b94d8425eb414cbe1623f9b0ab5d10d996101da7b71c2e8869a7037c747f1c325f31b7afb789df1fe434d808b2b5b55ff675153584c69d74b233f0c07d467ff202108d94fbc936b37359e971e1163cf36fc290dfa80738007eef64579dea09fdf1f21f279ee31749f0285fcfc163ac331375271212c9665b50ba0ea9d83c05'
    data = bytes.fromhex(data)

    request = _decodeSecurityRequest(data, header=[])
    print(request)

    returned_sig = validate_signature(
        pub_key_path,
        request['certificate'].get('raw_cert'),
        request['certificate'].get('raw_signature')
    )
    print(returned_sig)
