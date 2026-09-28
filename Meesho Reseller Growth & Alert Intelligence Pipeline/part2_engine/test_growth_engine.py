from pathlib import Path

from growth_engine import mom_growth, is_flagged, validate_feed


FIXTURES = Path(__file__).parent / "fixtures"


# Test 1
# GIVEN April -> May Ethnic Wear revenue changes
# WHEN we calculate growth and flag status
# THEN growth is 77.1% and it is flagged

def test_ethnic_wear_growth():
    growth = mom_growth(104520.77, 185107.61)

    assert growth == 77.1
    assert is_flagged(growth) == "flagged"


# Test 2
# GIVEN May -> June Beauty & Personal Care revenue changes
# WHEN we calculate growth and flag status
# THEN growth is 5.67% and it is not flagged

def test_beauty_growth():
    growth = mom_growth(35542.11, 37559.07)

    assert growth == 5.67
    assert is_flagged(growth) == "not_flagged"


# Test 3
# GIVEN exactly 8% growth
# WHEN we evaluate the threshold
# THEN it must be escalated for human review

def test_exact_boundary():
    growth = mom_growth(100000, 108000)

    assert growth == 8.0
    assert is_flagged(growth) == "escalate_exact_boundary"


# Test 4
# GIVEN the corrupted CSV feed
# WHEN we validate it
# THEN exactly 3 errors are returned in the required order

def test_corrupted_feed():
    csv_path = FIXTURES / "corrupted_feed.csv"

    valid, errors = validate_feed(str(csv_path))

    expected_errors = [
        "line 3: negative revenue (-4200.0) for category=Western Wear",
        "line 4: missing category (month=July)",
        "line 6: missing revenue (category=Home & Kitchen)",
    ]

    assert valid is False
    assert len(errors) == 3
    assert errors == expected_errors


# Additional check:
# The valid Part 1 CSV must pass the guardrail.

def test_valid_part1_feed():
    csv_path = FIXTURES / "monthly_category_revenue.csv"

    valid, errors = validate_feed(str(csv_path))

    assert valid is True
    assert errors == []
def test_full_may_vs_april():
    april = {
        "Ethnic Wear": 104520.77,
        "Western Wear": 113866.15,
        "Kids Wear": 59847.27,
        "Home & Kitchen": 100446.23,
        "Beauty & Personal Care": 40737.01,
    }

    may = {
        "Ethnic Wear": 185107.61,
        "Western Wear": 86998.18,
        "Kids Wear": 45793.78,
        "Home & Kitchen": 91152.57,
        "Beauty & Personal Care": 35542.11,
    }

    expected = {
        "Ethnic Wear": (77.1, "flagged"),
        "Western Wear": (-23.6, "flagged"),
        "Kids Wear": (-23.48, "flagged"),
        "Home & Kitchen": (-9.25, "flagged"),
        "Beauty & Personal Care": (-12.75, "flagged"),
    }

    for category in expected:
        growth = mom_growth(april[category], may[category])

        assert growth == expected[category][0]
        assert is_flagged(growth) == expected[category][1]
def test_full_june_vs_may():
    may = {
        "Ethnic Wear": 185107.61,
        "Western Wear": 86998.18,
        "Kids Wear": 45793.78,
        "Home & Kitchen": 91152.57,
        "Beauty & Personal Care": 35542.11,
    }

    june = {
        "Ethnic Wear": 76371.53,
        "Western Wear": 97415.64,
        "Kids Wear": 56737.78,
        "Home & Kitchen": 129971.22,
        "Beauty & Personal Care": 37559.07,
    }

    expected = {
        "Ethnic Wear": (-58.74, "flagged"),
        "Western Wear": (11.97, "flagged"),
        "Kids Wear": (23.9, "flagged"),
        "Home & Kitchen": (42.59, "flagged"),
        "Beauty & Personal Care": (5.67, "not_flagged"),
    }

    for category in expected:
        growth = mom_growth(may[category], june[category])

        assert growth == expected[category][0]
        assert is_flagged(growth) == expected[category][1]