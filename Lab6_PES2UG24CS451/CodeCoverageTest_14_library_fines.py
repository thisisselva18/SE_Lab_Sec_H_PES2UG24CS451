import pytest
from library_fines import late_fine, can_borrow, renewal_status


# ---------- late_fine ----------
def test_unknown_member_raises():
    with pytest.raises(ValueError):
        late_fine("alien", 5, False)

def test_negative_days_raises():
    with pytest.raises(ValueError):
        late_fine("student", -1, False)

def test_faculty_overdue_and_damaged():
    # 40 - 30 = 10 days late * 1 = 10, plus 150 damage
    assert late_fine("faculty", 40, True) == 160

def test_guest_fine_capped_at_200():
    # 100 - 14 = 86 days late * 5 = 430 -> capped at 200
    assert late_fine("guest", 100, False) == 200


# ---------- can_borrow ----------
def test_can_borrow():
    assert can_borrow(1, 0, "student") is True

def test_cannot_borrow_with_high_fine():
    assert can_borrow(0, 150, "student") is False

def test_faculty_can_borrow():
    assert can_borrow(5, 0, "faculty") is True


# ---------- renewal_status ----------
def test_renewal_denied_when_reserved():
    assert renewal_status(0, True, 5) == "denied"

def test_renewal_limit_reached():
    assert renewal_status(2, False, 5) == "limit reached"

def test_renewal_overdue():
    assert renewal_status(0, False, -1) == "overdue"

def test_renewal_success():
    assert renewal_status(0, False, 5) == "renewed"
