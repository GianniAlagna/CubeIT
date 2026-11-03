"""Run: python tests/test_cubetool.py"""
from __future__ import print_function
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
import cubetool as ct

for tid in ct.TYPES:
    rec = ct.build_record(tid, 123456, (2, 3))
    assert len(rec) == ct.RECORD_LEN and sum(rec) % 256 == 0
    out = ct.parse_record(rec)
    assert out["type_id"] == tid and out["serial"] == 123456 and out["rev"] == "2.3"
bad = bytearray(ct.build_record(0x03, 1)); bad[10] ^= 0xFF
for data, msg in ((bad, "checksum"), (b"\xff" * 32, "blank"), (b"\x00" * 10, "short")):
    try:
        ct.parse_record(data); raise AssertionError("should fail: " + msg)
    except ValueError as exc:
        assert msg in str(exc), exc
assert ct.main(["scan", "--simulate"]) == 0
print("ALL OK")
