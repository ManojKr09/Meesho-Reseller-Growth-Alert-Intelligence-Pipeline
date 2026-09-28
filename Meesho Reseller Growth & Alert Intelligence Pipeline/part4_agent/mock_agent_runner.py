import csv
import json
import sys
from pathlib import Path

# Allow this file to import Part 2's growth_engine.py
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PART2_ENGINE = PROJECT_ROOT / "part2_engine"

if str(PART2_ENGINE) not in sys.path:
    sys.path.insert(0, str(PART2_ENGINE))

from growth_engine import validate_feed, mom_growth, is_flagged


def load_feed(csv_path: str) -> dict:
    """Load category revenue from a monthly CSV."""
    data = {}

    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            category = (row.get("category") or "").strip()

            if category:
                data[category] = float(row["revenue"])

    return data


def get_month_from_csv(csv_path: str) -> str:
    """Read the month name from the CSV."""
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        first_row = next(reader, None)

        if first_row is None:
            return ""

        return (first_row.get("month") or "").strip()


def fill_prompt(
    category: str,
    previous_revenue: float,
    current_revenue: float,
    mom_pct: float,
    month: str,
    prev_month: str,
) -> str:
    """Fill the Part 3 narrative template using supplied values only."""

    return (
        f"Context: {category} revenue is being measured for "
        f"{month} versus {prev_month}.\n"
        f"Insight — Fact: {category} revenue changed from "
        f"{previous_revenue} in {prev_month} to {current_revenue} "
        f"in {month}, representing {mom_pct}% MoM growth.\n"
        f"Implication — Hypothesis: The change may reflect a change "
        f"in category-level demand or activity, but the supplied data "
        f"does not establish the cause. The regional manager should "
        f"check category order volume and relevant operational or "
        f"promotional activity before deciding on further action."
    )


def run(
    month: str,
    previous_month_csv: str,
    current_month_csv: str
) -> dict:
    """
    Execute the guarded Part 4 workflow.
    """

    # 1. Validate current feed first.
    valid, validation_errors = validate_feed(current_month_csv)

    result = {
        "run_month": month,
        "validation_status": "valid" if valid else "invalid",
        "validation_errors": validation_errors,
        "flagged_categories": [],
        "suppressed_categories": [],
        "escalated_categories": [],
        "action_taken": (
            "drafted_and_held_for_approval"
            if valid
            else "hard_stop"
        ),
    }

    # 2. Hard Stop if validation fails.
    if not valid:
        return result

    # 3. Load previous and current feeds.
    previous_data = load_feed(previous_month_csv)
    current_data = load_feed(current_month_csv)

    previous_month = get_month_from_csv(previous_month_csv)

    # 4. Calculate growth and classify every category.
    flagged = []
    escalated = []

    for category, current_revenue in current_data.items():

        if category not in previous_data:
            continue

        previous_revenue = previous_data[category]

        mom_pct = mom_growth(
            previous_revenue,
            current_revenue
        )

        status = is_flagged(mom_pct)

        if status == "flagged":

            flagged.append({
                "category": category,
                "mom_pct": mom_pct,
                "previous_revenue": previous_revenue,
                "current_revenue": current_revenue,
            })

        elif status == "escalate_exact_boundary":

            escalated.append(category)

    # 5. Sort flagged categories by absolute MoM magnitude.
    flagged.sort(
        key=lambda item: abs(item["mom_pct"]),
        reverse=True
    )

    # 6. Draft only the top 3.
    top_three = flagged[:3]

    for item in top_three:

        item["drafted"] = True

        item["message"] = fill_prompt(
            category=item["category"],
            previous_revenue=item["previous_revenue"],
            current_revenue=item["current_revenue"],
            mom_pct=item["mom_pct"],
            month=month,
            prev_month=previous_month,
        )

    # 7. Suppress remaining flagged categories.
    remaining = flagged[3:]

    suppressed = [
        item["category"]
        for item in remaining
    ]

    # 7b. Keep exact-boundary categories separate.
    result["flagged_categories"] = top_three
    result["suppressed_categories"] = suppressed
    result["escalated_categories"] = escalated

    # 8. Return one structured object.
    return result


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(
        description="Run the guarded Meesho monitoring agent."
    )

    parser.add_argument("month")
    parser.add_argument("previous_month_csv")
    parser.add_argument("current_month_csv")

    args = parser.parse_args()

    output = run(
        args.month,
        args.previous_month_csv,
        args.current_month_csv
    )

    print(json.dumps(output, indent=2))