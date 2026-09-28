from masking import alias_for, assert_no_raw_names_leak


def test_alias_for():
    assert alias_for("RS019") == "ALIAS-19"
    assert alias_for("RS006") == "ALIAS-06"


def test_no_raw_names_leak():
    reseller_names = [
        "Mumbai Reseller 1",
        "Bengaluru Reseller 2",
        "Chennai Reseller 3",
        "Delhi Reseller 4",
        "Kolkata Reseller 5",
    ]

    safe_narrative = """
    In the South region, ALIAS-12 had the highest verified total spend
    among the reviewed reseller records.
    """

    assert assert_no_raw_names_leak(
        safe_narrative,
        reseller_names
    ) is True


def test_raw_name_is_detected():
    reseller_names = [
        "Mumbai Reseller 1",
        "Bengaluru Reseller 2",
    ]

    unsafe_narrative = """
    Mumbai Reseller 1 had the highest total spend.
    """

    assert assert_no_raw_names_leak(
        unsafe_narrative,
        reseller_names
    ) is False