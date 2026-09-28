\# Meesho Reseller-Ops Analytics \& Guarded Agent Workflow



\## Project Overview



This project implements a repeatable Meesho reseller-operations analytics workflow across four parts:



\* \*\*Part 1:\*\* Generate a deterministic reseller/order dataset and answer five business questions using SQL.

\* \*\*Part 2:\*\* Validate the monthly revenue feed and calculate Month-on-Month growth with an explicit 8% flagging threshold.

\* \*\*Part 3:\*\* Convert verified numbers into reliable stakeholder narratives using a reusable prompt pack and reseller-name masking.

\* \*\*Part 4:\*\* Combine Parts 1–3 into a guarded mock monitoring agent with validation, growth detection, notification limits, human approval, and structured JSON output.



The complete pipeline runs locally with \*\*zero API keys\*\* and does not make network calls or send real messages.



\---



\## Project Structure



```text

meesho\_part1/

│

├── data/

│   ├── generate\_dataset.py

│   ├── resellers.csv

│   ├── orders.csv

│   └── meesho\_reseller.db

│

├── part1\_sql/

│   ├── queries.sql

│   └── output/

│       ├── monthly\_category\_revenue.csv

│       ├── region\_revenue\_orders.csv

│       ├── top\_resellers.csv

│       ├── zero\_order\_resellers.csv

│       ├── zero\_order\_count\_demo.csv

│       └── june\_delivered\_aov.csv

│

├── part2\_engine/

│   ├── growth\_engine.py

│   ├── test\_growth\_engine.py

│   └── fixtures/

│       ├── corrupted\_feed.csv

│       ├── monthly\_category\_revenue.csv

│       ├── april\_revenue.csv

│       ├── may\_revenue.csv

│       └── june\_revenue.csv

│

├── part3\_narrative/

│   ├── prompt\_pack.md

│   ├── narrative\_report.md

│   ├── masking.py

│   └── test\_masking.py

│

├── part4\_agent/

│   ├── agent\_spec.md

│   ├── mock\_agent\_runner.py

│   └── test\_mock\_agent\_runner.py

│

└── README.md

```



\---



\## Requirements



\* Python 3.x

\* SQLite / SQLiteStudio for inspecting the database

\* pytest for running the automated tests



No API key is required.



No external API, email service, Gmail, SMTP service, or network integration is used.



\---



\# Part 1 — Dataset \& SQL Analysis



\## 1. Regenerate the dataset



The dataset is deterministic because the generator uses a fixed random seed.



From the project root:



```bash

python data/generate\_dataset.py

```



This regenerates:



```text

data/resellers.csv

data/orders.csv

data/meesho\_reseller.db

```



The generator should be run without modifying its seed, weights, row counts, or other supplied parameters.



\## 2. Run the SQL analysis



Open:



```text

data/meesho\_reseller.db

```



in SQLiteStudio or another SQLite client.



Run the queries in:



```text

part1\_sql/queries.sql

```



The five analyses are:



1\. Monthly revenue by category

2\. Region-wise total revenue and order count

3\. Top resellers by total spend

4\. Resellers with no orders

5\. June Delivered Average Order Value



The verified outputs are stored in:



```text

part1\_sql/output/

```



Part 1 establishes the verified numerical source that is consumed by the later parts.



\---



\# Part 2 — Python Guardrail \& Growth Engine



The growth engine is implemented in:



```text

part2\_engine/growth\_engine.py

```



It provides:



\* `mom\_growth()`

\* `is\_flagged()`

\* `validate\_feed()`



The 8% threshold is explicit:



\* Above 8% absolute growth → `flagged`

\* Below 8% absolute growth → `not\_flagged`

\* Exactly 8% absolute growth → `escalate\_exact\_boundary`



Run the Part 2 tests:



```bash

python -m pytest part2\_engine

```



The tests include normal growth cases, the exact 8% boundary, corrupted-feed validation, and the full May/June acceptance tables.



Part 1 → Part 2 mirrors the workflow pattern of \*\*compute real numbers via SQL first, then hand off verified data to a guarded Python decision engine\*\*.



\---



\# Part 3 — Reliable AI Narrative \& Prompt Pack



Part 3 contains:



```text

part3\_narrative/prompt\_pack.md

part3\_narrative/narrative\_report.md

part3\_narrative/masking.py

part3\_narrative/test\_masking.py

```



The prompt pack defines a reusable:



```text

Trigger → Input List → Prompt → Checklist

```



workflow.



The narrative report converts verified Part 1/Part 2 numbers into:



```text

Context → Insight → Implication

```



while distinguishing facts from hypotheses.



Reseller names are protected using coded aliases such as:



```text

RS019 → ALIAS-19

RS006 → ALIAS-06

```



Run the Part 3 tests:



```bash

python -m pytest part3\_narrative

```



Part 3 mirrors a \*\*verified-data → narrative drafting → validation/masking\*\* reporting workflow.



\---



\# Part 4 — Agentic Workflow \& Mock Runner



Part 4 combines the previous parts into a guarded monitoring workflow.



The agent:



1\. Loads the monthly revenue feed.

2\. Validates the input.

3\. Hard Stops if validation fails.

4\. Calculates MoM growth using the unchanged Part 2 engine.

5\. Classifies every category.

6\. Sorts flagged categories by absolute MoM magnitude.

7\. Drafts messages for at most the top three flagged categories.

8\. Suppresses additional flagged categories for manual review.

9\. Separately records exact-boundary categories for human review.

10\. Returns one structured JSON object.



The implementation is:



```text

part4\_agent/mock\_agent\_runner.py

```



No message is actually sent. Drafts are held for human approval.



Run the Part 4 tests:



```bash

python -m pytest part4\_agent

```



Part 4 mirrors an \*\*Intake → Summary → Report Draft → Validate → Human Approval\*\* workflow.



\---



\# Run the Complete Test Suite



From the project root:



```bash

python -m pytest part2\_engine part3\_narrative part4\_agent

```



The completed project currently passes the integrated test suite with:



```text

15 passed

```



\---



\# Complete Workflow



```text

Part 1

Deterministic Dataset

&#x20;       ↓

SQL Business Analysis

&#x20;       ↓

Verified Revenue Output

&#x20;       ↓

Part 2

Input Validation

&#x20;       ↓

MoM Growth Calculation

&#x20;       ↓

8% Flagging / Boundary Escalation

&#x20;       ↓

Part 3

Reliable Narrative

&#x20;       ↓

Fact / Hypothesis Separation

&#x20;       ↓

Privacy Masking

&#x20;       ↓

Part 4

Guarded Agent

&#x20;       ↓

Top-3 Draft Limit

&#x20;       ↓

Suppression / Escalation

&#x20;       ↓

Human Approval

&#x20;       ↓

Structured JSON Output

```



\## Zero API Keys



The entire pipeline runs locally with \*\*zero API keys configured\*\*.



There are:



\* No OpenAI API calls

\* No external AI API calls

\* No Gmail/SMTP integration

\* No network calls

\* No real message sending



All calculations, validation, narrative generation, masking, testing, and mock-agent execution are performed locally.



