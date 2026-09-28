import csv


def mom_growth(previous: float, current: float) -> float:
    return round((current - previous) / previous * 100, 2)


def is_flagged(mom_pct: float, threshold: float = 8.0) -> str:
    if abs(mom_pct) > threshold:
        return "flagged"
    elif abs(mom_pct) < threshold:
        return "not_flagged"
    else:
        return "escalate_exact_boundary"


def validate_feed(csv_path: str) -> tuple[bool, list[str]]:
    errors = []

    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for line_no, row in enumerate(reader, start=2):
            month = (row.get("month") or "").strip()
            category = (row.get("category") or "").strip()
            revenue_raw = row.get("revenue")

            if category == "":
                errors.append(
                    f"line {line_no}: missing category (month={month})"
                )

            if revenue_raw is None or revenue_raw.strip() == "":
                errors.append(
                    f"line {line_no}: missing revenue (category={category})"
                )
                continue

            revenue_text = revenue_raw.strip()

            try:
                revenue = float(revenue_text)
            except ValueError:
                errors.append(
                    f"line {line_no}: revenue not numeric: {revenue_text!r}"
                )
                continue

            if revenue < 0:
                errors.append(
                    f"line {line_no}: negative revenue ({revenue}) "
                    f"for category={category}"
                )

    return (len(errors) == 0, errors)