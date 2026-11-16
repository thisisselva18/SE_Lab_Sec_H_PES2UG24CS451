"""
Lab 7 - Fuzz testing library_fines.py with Hypothesis.

Contract the hardened functions must satisfy:
  * They never raise, whatever they are given (str, None, int, list, ...).
  * Invalid input returns None.
  * Valid input returns the correct value.
"""
import re
import string

from hypothesis import given, settings, strategies as st

from library_fines import parse_member_id, total_fine, shelf_code

# Anything a caller could pass in: random Unicode text, None, or a wrong type.
any_input = st.one_of(
    st.text(),
    st.none(),
    st.integers(),
    st.floats(),
    st.binary(),
    st.lists(st.text()),
)

ascii_letters = st.text(alphabet=string.ascii_letters, min_size=1, max_size=10)
ascii_digits = st.text(alphabet=string.digits, min_size=1, max_size=9)


# --------------------------------------------------------------------------
# parse_member_id
# --------------------------------------------------------------------------
@given(st.text() | st.none())
def test_parse_member_id_no_crash(s):
    try:
        parse_member_id(s)
    except Exception as e:
        assert False, f"parse_member_id crashed with: {type(e).__name__}: {e}"


@given(any_input)
def test_parse_member_id_wrong_types_no_crash(s):
    try:
        parse_member_id(s)
    except Exception as e:
        assert False, f"parse_member_id crashed with: {type(e).__name__}: {e}"


@given(ascii_letters, ascii_digits)
def test_parse_member_id_valid_round_trip(member_type, number):
    # A well-formed ID like "stu-0042" must parse to ("STU", 42).
    assert parse_member_id(f"{member_type}-{number}") == (member_type.upper(), int(number))


@given(st.text())
def test_parse_member_id_result_is_well_formed(s):
    # Whatever comes back must be None or (ASCII-uppercase type, non-negative int).
    result = parse_member_id(s)
    if result is not None:
        member_type, number = result
        assert re.fullmatch(r"[A-Z]+", member_type), f"bad member type {member_type!r}"
        assert isinstance(number, int) and number >= 0


# --------------------------------------------------------------------------
# total_fine
# --------------------------------------------------------------------------
@given(st.text() | st.none())
def test_total_fine_no_crash(s):
    try:
        total_fine(s)
    except Exception as e:
        assert False, f"total_fine crashed with: {type(e).__name__}: {e}"


@given(any_input)
def test_total_fine_wrong_types_no_crash(s):
    try:
        total_fine(s)
    except Exception as e:
        assert False, f"total_fine crashed with: {type(e).__name__}: {e}"


@given(st.lists(st.integers(min_value=0, max_value=3650), min_size=1, max_size=50))
def test_total_fine_matches_fine_rule(days):
    # Rs 2 per day for every day beyond the 14-day loan period.
    expected = sum((d - 14) * 2 for d in days if d > 14)
    assert total_fine(",".join(map(str, days))) == expected


@given(st.lists(st.integers(min_value=0, max_value=3650), min_size=1, max_size=50),
       st.integers(min_value=-10**6, max_value=-1))
def test_total_fine_rejects_negative_days(days, negative):
    # A book cannot be kept for a negative number of days.
    days.append(negative)
    assert total_fine(",".join(map(str, days))) is None


@given(st.text())
@settings(max_examples=300)
def test_total_fine_result_is_none_or_non_negative_int(s):
    result = total_fine(s)
    assert result is None or (isinstance(result, int) and result >= 0)


# --------------------------------------------------------------------------
# shelf_code
# --------------------------------------------------------------------------
@given(st.text() | st.none())
def test_shelf_code_no_crash(s):
    try:
        shelf_code(s)
    except Exception as e:
        assert False, f"shelf_code crashed with: {type(e).__name__}: {e}"


@given(any_input)
def test_shelf_code_wrong_types_no_crash(s):
    try:
        shelf_code(s)
    except Exception as e:
        assert False, f"shelf_code crashed with: {type(e).__name__}: {e}"


@given(st.lists(ascii_letters, min_size=2, max_size=6))
def test_shelf_code_valid_titles(words):
    title = " ".join(words)
    assert shelf_code(title) == (words[0][0] + words[1][0]).upper()


@given(st.text())
@settings(max_examples=300)
def test_shelf_code_is_two_characters(s):
    # A shelf code is always exactly two letters/digits (or None if the title is unusable).
    result = shelf_code(s)
    if result is not None:
        assert len(result) == 2, f"shelf code {result!r} is not 2 characters"
        assert all(ch.isalnum() for ch in result), f"shelf code {result!r} has symbols"
