
from hypothesis import given, strategies as st

from processor import (
    verify_isbn10_format,
    calculate_depreciation_factor,
    lookup_condition_multiplier
)


# Test 1: ISBN-10 format validation
@given(st.one_of(st.text(), st.none()))
def test_verify_isbn10_format_no_crash(s):
    try:
        verify_isbn10_format(s)
    except Exception as e:
        assert False, f"ISBN function crashed with input {s!r}: {e}"


# Test 2: Depreciation factor calculation
@given(st.one_of(st.text(), st.none()))
def test_calculate_depreciation_factor_safe(s):
    try:
        calculate_depreciation_factor(s)
    except Exception as e:
        assert False, f"Depreciation function crashed with input {s!r}: {e}"


# Test 3: Condition multiplier lookup
@given(st.one_of(st.text(), st.none()))
def test_lookup_condition_multiplier_safe(s):
    try:
        lookup_condition_multiplier(s)
    except Exception as e:
        assert False, f"Condition function crashed with input {s!r}: {e}"
