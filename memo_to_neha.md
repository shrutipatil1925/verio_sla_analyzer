# Memo — First-response SLA breaches

**To:** Neha Kulkarni, Support Operations Manager
**Subject:** Vireo Audio first-response SLA breach findings

## Executive summary

The analysis covers **11,200 unique tickets** after removing 616 duplicate records. Across all tickets, **2,440 breached the first-response target (21.8%)**. Among completed tickets, **2,320 breaches occurred (21.9%)**, representing **₹8.12 lakh in SLA-credit exposure** under the current ₹350-per-breach policy.

The **Morning shift has the highest observed breach rate at 32.2%**, compared with 8.4% for Day and 10.8% for Night. Morning accounts for **2,018 of the 2,440 breaches (82.7%)**. Within the Morning shift, chat has a **41.3% breach rate**.

## Business impact

The current policy automatically issues a **₹350 store credit for each first-response breach when the ticket is resolved**.

At the observed completed-ticket breach rate of 21.9%, a volume of approximately **650 tickets per week** would correspond to an estimated **142 breaches per week**, or about **₹49,700 in weekly SLA-credit exposure**. This is approximately **₹2.16 lakh per month** if the observed rate and ticket volume remain similar. This is an estimate, not a guaranteed future cost.

## What to investigate first

1. Review Morning-shift chat coverage and arrival volume by hour.
2. Check whether the Morning shift inherits unresolved work from the previous shift.
3. Review recurring agent/shift patterns using both breach count and breach rate rather than volume alone.
4. Monitor the weekly shift and agent reports to determine whether the Morning pattern persists.

## Reporting decisions and limitations

* Timestamps were converted from UTC to IST before applying the roster and weekly reporting logic.
* Duplicate ticket IDs were treated as migration re-imports, with the helpdesk copy retained.
* A response exactly at the SLA target is **not** counted as a breach.
* The support email mentions approximately 40 failed IVR transcripts, but the supplied data does not contain a reliable structured field identifying them. They were therefore **not silently excluded**. If Vireo provides an authoritative list, the report can be rerun and the difference documented.
* The June roster reshuffle is not treated as causal because the available post-change period is insufficient to establish causation.
* Tier 2 is not compared with Tier 1 on volume metrics, consistent with the support policy.
