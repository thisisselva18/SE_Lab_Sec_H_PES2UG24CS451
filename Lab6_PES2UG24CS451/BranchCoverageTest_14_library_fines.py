import pytest
from library_fines import late_fine, can_borrow, renewal_status


# ---------- late_fine ----------
def test_returned_on_time():
    # overdue <= 0 -> skips the fine block (False branch of "overdue > 0")
    assert late_fine("student", 10, False) == 0

def test_unknown_member_raises():
    with pytest.raises(ValueError):
        late_fine("alien", 5, False)

def test_negative_days_raises():
    with pytest.raises(ValueError):
        late_fine("student", -1, False)

def test_zero_days_is_valid():
    assert late_fine("student", 0, False) == 0

def test_student_returned_on_last_day():
    assert late_fine("student", 14, False) == 0

def test_student_one_day_late():
    assert late_fine("student", 15, False) == 2

def test_faculty_returned_on_last_day():
    assert late_fine("faculty", 30, False) == 0

def test_faculty_overdue_and_damaged():
    # 40 - 30 = 10 days late * 1 = 10, plus 150 damage
    assert late_fine("faculty", 40, True) == 160

def test_guest_fine_exactly_200_not_capped():
    # 54 - 14 = 40 days late * 5 = 200 (not > 200)
    assert late_fine("guest", 54, False) == 200

def test_guest_fine_capped_at_200():
    # 100 - 14 = 86 days late * 5 = 430 -> capped at 200
    assert late_fine("guest", 100, False) == 200

def test_damaged_but_on_time():
    assert late_fine("student", 5, True) == 150

def test_capped_fine_plus_damage():
    assert late_fine("guest", 100, True) == 350


# ---------- can_borrow ----------
def test_can_borrow():
    assert can_borrow(1, 0, "student") is True

def test_cannot_borrow_with_high_fine():
    assert can_borrow(0, 150, "student") is False

def test_can_borrow_with_fine_exactly_100():
    assert can_borrow(0, 100, "student") is True

def test_student_at_book_limit():
    assert can_borrow(3, 0, "student") is False

def test_faculty_can_borrow():
    assert can_borrow(5, 0, "faculty") is True

def test_faculty_at_book_limit():
    assert can_borrow(10, 0, "faculty") is False

def test_faculty_with_high_fine():
    assert can_borrow(0, 101, "faculty") is False


# ---------- renewal_status ----------
def test_renewal_denied_when_reserved():
    assert renewal_status(0, True, 5) == "denied"

def test_reservation_checked_before_limit():
    assert renewal_status(5, True, -3) == "denied"

def test_renewal_limit_reached():
    assert renewal_status(2, False, 5) == "limit reached"

def test_limit_checked_before_overdue():
    assert renewal_status(3, False, -1) == "limit reached"

def test_renewal_overdue():
    assert renewal_status(0, False, -1) == "overdue"

def test_renewal_success():
    assert renewal_status(0, False, 5) == "renewed"

def test_renewal_on_due_date():
    assert renewal_status(1, False, 0) == "renewed"
