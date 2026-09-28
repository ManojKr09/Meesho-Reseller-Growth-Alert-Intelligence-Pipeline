# Part 4 — Agent Specification

## 4.1 Five Core Components

### Goal

Keep Meesho category managers informed of category month-on-month revenue movements beyond the 8% threshold, while ensuring every drafted message is held for human approval before it can be considered sent.

### Tools

The monitoring agent calls these concrete functions:

1. `validate_feed` from Part 2 — validates the monthly revenue CSV before any analysis.
2. `mom_growth` from Part 2 — calculates month-on-month revenue growth.
3. `is_flagged` from Part 2 — classifies each growth result as `flagged`, `not_flagged`, or `escalate_exact_boundary`.
4. Part 3 prompt-pack template-fill logic — creates a stakeholder narrative using the verified category, revenue, month, previous month, and MoM values.

The Part 2 growth-engine functions are imported and reused without modification.

### Memory / State

Between runs, the agent needs the previous month's verified revenue for each category so that the next run can calculate month-on-month growth.

The state concept is:

```text
category -> previous month's verified revenue