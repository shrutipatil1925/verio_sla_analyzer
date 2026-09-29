# 3-Minute Screen Recording Script

## 0:00–0:20 — Project and task context

Show the project folder and `README.md`.

Say:

> “This is my Vireo Audio first-response SLA reporting tool. It analyzes support tickets against the supplied SLA policy and generates weekly shift, agent, and channel reports.”

## 0:20–0:45 — Policy and assumptions

Open `README.md` or `support-policy.pdf`.

Show:

* Channel SLA targets
* UTC → IST conversion
* ₹350 SLA credit
* Morning, Day, and Night shifts
* Duplicate handling

Say:

> “The tool applies the supplied policy rules. Timestamps are converted from UTC to IST, duplicate ticket IDs are handled deterministically, and a response exactly at the SLA target is not treated as a breach.”

## 0:45–1:10 — Run the tool

Open PowerShell and run:

```powershell
python -u vireo_sla_report.py --data data --out outputs
```

Show the terminal output.

Point out:

* 11,816 raw rows
* 11,200 unique tickets
* 616 duplicates removed
* 2,440 breaches
* 21.79% overall breach rate
* 2,320 completed breaches
* ₹812,000 completed credit exposure
* QA checks

## 1:10–1:45 — Show the useful outputs

Open:

* `overall_summary.csv`
* `weekly_shift.csv`
* `channel_shift_summary.csv`

Say:

> “The main finding is that the Morning shift has the highest observed breach rate at 32.2% and accounts for 82.7% of all breaches. Morning chat has a 41.3% breach rate.”

Show the weekly report briefly to demonstrate that the analysis is not only an overall total.

## 1:45–2:10 — Agent-level report

Open:

`outputs/weekly_agent_shift.csv`

Say:

> “This report provides agent and shift-level breach counts and rates. I use it to identify recurring patterns, but I do not treat the results as proof of individual causation.”

Show a few rows.

## 2:10–2:30 — QA and limitations

Open:

`outputs/qa_report.json`

Show:

* missing responses = 0
* missing agents = 0
* negative response times = 0
* unmatched roster rows = 0

Then say:

> “The supplied email mentions failed IVR transcripts, but there is no reliable structured field to identify those tickets, so I did not silently exclude them.”

## 2:30–2:50 — AI use and discarded work

Open:

`prompts_used.md`

Say:

> “I used ChatGPT for development review, QA challenges, and documentation. The runtime calculations are deterministic Python. I removed unsupported conclusions, including an unsupported 15% target and causal claims about the roster reshuffle.”

## 2:50–3:00 — Manager memo

Open:

`memo_to_neha.md`

Say:

> “The final memo summarizes the findings, estimated business impact, investigation priorities, and important limitations for the Support Operations Manager.”

End recording.
