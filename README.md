# Vireo Audio — First-Response SLA Reporting Tool

A reproducible Python CLI that analyzes Vireo Audio support tickets and produces weekly first-response SLA reports by agent, shift, and channel.

## Business Purpose

The tool helps Support Operations identify where first-response SLA breaches are concentrated and quantify the associated SLA-credit exposure.

For the supplied assessment dataset:

* **11,200 unique tickets** after removing **616 migration duplicate rows**
* **2,440 total first-response SLA breaches**
* **21.79% overall breach rate**
* **2,320 completed-ticket breaches**
* **₹8.12 lakh** in completed-ticket SLA-credit exposure at the policy rate of **₹350 per breach**

The report is designed to help the support team focus investigation and operational review on the shifts, channels, and agent/shift combinations where breaches are concentrated.

## Setup

### 1. Create a virtual environment

PowerShell:

```powershell
python -m venv .venv
```

### 2. Activate the environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run the following for the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Run the report

The assessment input files are supplied separately and are intentionally excluded from the public GitHub repository.

Place the supplied `data/` directory in the project root, then run:

```powershell
python vireo_sla_report.py --data data --out outputs
```

## What the Tool Produces

The `outputs/` directory contains:

* `overall_summary.csv` — headline SLA and financial metrics
* `weekly_summary.csv` — weekly breach summary
* `weekly_shift.csv` — weekly results by shift
* `weekly_agent_shift.csv` — weekly results by agent and shift
* `agent_summary.csv` — agent-level summary
* `channel_shift_summary.csv` — channel and shift breakdown
* `scored_tickets.csv` — ticket-level SLA calculations
* `qa_report.json` — validation and data-quality checks

## SLA Rules

The calculations use the supplied support policy:

| Channel | First-response target |
| ------- | --------------------: |
| Chat    |            15 minutes |
| Voice   |               2 hours |
| Social  |               4 hours |
| Email   |               8 hours |

A ticket is a **breach** when its first response is strictly later than the applicable target.

The policy specifies a **₹350 store credit** for each ticket that misses its first-response target and is resolved.

## Reporting Logic and Assumptions

* API timestamps are UTC and are converted to IST for roster matching and weekly reporting.
* Duplicate ticket IDs are treated as migration re-imports; the helpdesk copy is preferred.
* Agent roster assignment uses the roster row active on the first-response date.
* Completed tickets are those with `resolved` or `closed` status.
* Open and pending tickets remain visible in operational SLA metrics but are not counted as realized SLA-credit exposure.
* Tier 2 remains visible in the reports but is not benchmarked against Tier 1 on volume.
* The tool identifies where breaches occur; it does not claim that the observed patterns establish a causal reason.

## Validation

The supplied assessment dataset produces:

* **11,816** raw ticket rows
* **11,200** unique tickets after deduplication
* **616** duplicate rows removed
* **2,440** total first-response breaches
* **21.79%** overall breach rate
* **10,611** completed tickets
* **2,320** completed-ticket breaches
* **21.86%** completed-ticket breach rate
* **₹812,000** completed-ticket SLA-credit exposure
* **0** missing first-response timestamps
* **0** missing agent IDs
* **0** negative response intervals
* **0** unmatched roster assignments

## Project Structure

```text
vireo_sla_analyzer/
│
├── data/                       # Supplied assessment data; not committed
│
├── outputs/                    # Generated reports; not committed
│
├── tests/
│
├── vireo_sla_report.py
├── requirements.txt
├── README.md
├── memo_to_neha.md
├── prompts_used.md
├── screen_recording_script.md
├── submission-form-draft.md
└── .gitignore
```

## Scope

The core SLA calculations are deterministic Python calculations. AI was used during development for analysis, code review, QA, and drafting supporting documentation.

The model is **not** used to decide whether a ticket breached its SLA. Breach classification, deduplication, roster matching, aggregation, and financial calculations are implemented deterministically in Python.

## Data Privacy

The supplied assessment data contains operational and customer-related information. The public repository therefore excludes the supplied CSV files, policy document, email thread, and generated outputs.

The assessment data should be placed in the local `data/` directory when running the tool.
