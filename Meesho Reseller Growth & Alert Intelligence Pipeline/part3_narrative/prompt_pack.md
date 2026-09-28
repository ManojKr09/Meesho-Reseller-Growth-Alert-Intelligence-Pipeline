# Reusable Prompt Pack — Flagged Category Narrative

## Trigger

Start this prompt when a category's `is_flagged` result is exactly `"flagged"`.

## Input list

The prompt requires these placeholder variables:

- `{category}` — the category being analyzed
- `{previous_revenue}` — revenue in the previous month
- `{current_revenue}` — revenue in the current month
- `{mom_pct}` — calculated Month-on-Month growth percentage
- `{month}` — current month
- `{prev_month}` — previous month

## Prompt

Write a concise stakeholder update for a regional manager using the Context → Insight → Implication structure.

Context:
State what `{category}` revenue is being measured and explicitly name the comparison period `{month}` versus `{prev_month}`.

Insight:
State the supplied `{mom_pct}` as a fact and include the supplied `{previous_revenue}` and `{current_revenue}` values where relevant. Do not calculate, invent, round, or introduce any number that is not supplied in the input placeholders.

Implication:
Give one specific and actionable next step for the regional manager. If proposing a possible explanation for the change, label it explicitly as a hypothesis because the supplied data does not prove causation.

Data integrity:
Use only the supplied placeholder values. Never state a number that is not one of the supplied placeholders. Do not invent causes, events, customers, resellers, or operational facts.

Privacy:
If a reseller is mentioned, use only its coded alias and never expose the raw reseller name.

## Checklist

Before the narrative is used, verify all of the following:

1. Every number in the narrative exactly matches a supplied placeholder value.
2. The comparison explicitly names `{month}` versus `{prev_month}`.
3. The Insight is labeled as a fact.
4. Any proposed cause or explanation is explicitly labeled as a hypothesis.
5. The Implication contains a specific, actionable next step rather than a vague recommendation.
6. No raw reseller name appears in the narrative; only a coded alias may be used.
7. The narrative follows the Context → Insight → Implication structure.
8. The narrative is written for a regional manager rather than a technical/data-engineering audience.