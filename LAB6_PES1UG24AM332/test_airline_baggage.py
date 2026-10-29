import pytest
from airline_baggage import baggage_fee, carry_on_ok, check_in_status


# ---------------- Baggage fee tests ----------------

def test_within_allowance():
    assert baggage_fee("economy", 10, "domestic", False) == 0


def test_unknown_cabin():
    with pytest.raises(ValueError, match="unknown cabin"):
        baggage_fee("first", 10, "domestic", False)


def test_negative_weight():
    with pytest.raises(ValueError, match="invalid weight"):
        baggage_fee("economy", -1, "domestic", False)


def test_member_gets_extra_allowance():
    assert baggage_fee("economy", 20, "domestic", True) == 0


def test_business_member_gets_no_extra_allowance():
    assert baggage_fee("business", 45, "domestic", True) == 100


def test_domestic_baggage_fee():
    assert baggage_fee("economy", 20, "domestic", False) == 100


def test_international_baggage_fee():
    assert baggage_fee("premium", 30, "international", False) == 225


def test_excess_over_20_kg_domestic():
    assert baggage_fee("economy", 36, "domestic", False) == 840


def test_excess_over_20_kg_international():
    assert baggage_fee("premium", 50, "international", False) == 2500


# ---------------- Carry-on tests ----------------

def test_carry_on_ok():
    assert carry_on_ok(5, 1, False) is True


def test_infant_can_carry_two_items():
    assert carry_on_ok(10, 2, True) is True


def test_infant_cannot_carry_three_items():
    assert carry_on_ok(5, 3, True) is False


def test_carry_on_overweight():
    assert carry_on_ok(8, 1, False) is False


def test_carry_on_at_weight_limit():
    assert carry_on_ok(7, 1, False) is True


def test_carry_on_too_many_items():
    assert carry_on_ok(7, 2, False) is False


# ---------------- Check-in status tests ----------------

@pytest.mark.parametrize(
    "minutes,has_baggage,is_international,expected",
    [
        (60, True, False, "open"),
        (45, True, False, "late"),
        (44, True, False, "closed"),
        (45, False, False, "open"),
        (30, False, False, "late"),
        (29, False, False, "closed"),
        (120, True, True, "open"),
        (105, True, True, "late"),
        (104, True, True, "closed"),
        (105, False, True, "open"),
        (90, False, True, "late"),
        (89, False, True, "closed"),
    ],
)
def test_check_in_status(minutes, has_baggage, is_international, expected):
    assert check_in_status(
        minutes, has_baggage, is_international
    ) == expected
