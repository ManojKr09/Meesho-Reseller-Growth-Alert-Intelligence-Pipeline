from pathlib import Path

from mock_agent_runner import run


PROJECT_ROOT = Path(__file__).resolve().parent.parent

FIXTURES = PROJECT_ROOT / "part2_engine" / "fixtures"

APRIL = FIXTURES / "april_revenue.csv"
MAY = FIXTURES / "may_revenue.csv"
JUNE = FIXTURES / "june_revenue.csv"
CORRUPTED = FIXTURES / "corrupted_feed.csv"


def test_may_scenario():

    result = run(
        "May",
        str(APRIL),
        str(MAY),
    )

    assert result["validation_status"] == "valid"

    assert len(result["flagged_categories"]) == 3

    assert [
        item["category"]
        for item in result["flagged_categories"]
    ] == [
        "Ethnic Wear",
        "Western Wear",
        "Kids Wear",
    ]

    assert [
        item["mom_pct"]
        for item in result["flagged_categories"]
    ] == [
        77.1,
        -23.6,
        -23.48,
    ]

    assert all(
        item["drafted"] is True
        for item in result["flagged_categories"]
    )

    assert set(result["suppressed_categories"]) == {
        "Beauty & Personal Care",
        "Home & Kitchen",
    }

    assert result["escalated_categories"] == []

    assert result["action_taken"] == (
        "drafted_and_held_for_approval"
    )

    # Every drafted message must contain its category
    # and exact MoM percentage.
    for item in result["flagged_categories"]:
        assert item["category"] in item["message"]
        assert str(item["mom_pct"]) in item["message"]


def test_june_scenario():

    result = run(
        "June",
        str(MAY),
        str(JUNE),
    )

    assert result["validation_status"] == "valid"

    assert len(result["flagged_categories"]) == 3

    assert [
        item["category"]
        for item in result["flagged_categories"]
    ] == [
        "Ethnic Wear",
        "Home & Kitchen",
        "Kids Wear",
    ]

    assert [
        item["mom_pct"]
        for item in result["flagged_categories"]
    ] == [
        -58.74,
        42.59,
        23.9,
    ]

    assert all(
        item["drafted"] is True
        for item in result["flagged_categories"]
    )

    assert result["suppressed_categories"] == [
        "Western Wear"
    ]

    # Beauty & Personal Care is only 5.67%,
    # so it must not appear anywhere in either list.
    assert "Beauty & Personal Care" not in (
        result["suppressed_categories"]
    )

    assert "Beauty & Personal Care" not in [
        item["category"]
        for item in result["flagged_categories"]
    ]

    assert result["escalated_categories"] == []

    assert result["action_taken"] == (
        "drafted_and_held_for_approval"
    )


def test_corrupted_feed_hard_stop():

    result = run(
        "July",
        str(MAY),
        str(CORRUPTED),
    )

    assert result["validation_status"] == "invalid"

    assert result["action_taken"] == "hard_stop"

    assert result["validation_errors"] == [
        "line 3: negative revenue (-4200.0) for category=Western Wear",
        "line 4: missing category (month=July)",
        "line 6: missing revenue (category=Home & Kitchen)",
    ]

    assert result["flagged_categories"] == []

    assert result["suppressed_categories"] == []

    assert result["escalated_categories"] == []


def test_json_top_level_keys():

    result = run(
        "May",
        str(APRIL),
        str(MAY),
    )

    assert set(result.keys()) == {
        "run_month",
        "validation_status",
        "validation_errors",
        "flagged_categories",
        "suppressed_categories",
        "escalated_categories",
        "action_taken",
    }
def test_exact_boundary_is_escalated(tmp_path):

    previous = tmp_path / "previous.csv"
    current = tmp_path / "current.csv"

    previous.write_text(
        "month,category,revenue,n_orders\n"
        "April,Boundary Category,100000,10\n",
        encoding="utf-8",
    )

    current.write_text(
        "month,category,revenue,n_orders\n"
        "May,Boundary Category,108000,10\n",
        encoding="utf-8",
    )

    result = run(
        "May",
        str(previous),
        str(current),
    )

    assert result["validation_status"] == "valid"

    assert result["flagged_categories"] == []

    assert result["suppressed_categories"] == []

    assert result["escalated_categories"] == [
        "Boundary Category"
    ]

    assert result["action_taken"] == (
        "drafted_and_held_for_approval"
    )