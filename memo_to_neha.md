# Memo — First-response SLA breaches
**To:** Neha Kulkarni, Support Operations Manager

Across **11,200 unique tickets**, completed-ticket first-response breaches are **21.9%**; the operational rate across all tickets is **21.8%**.

The Morning shift is **32.2% breached**, versus **8.4%** Day and **10.8%** Night. Morning accounts for **2018 of 2440 breaches (82.7%)**. Morning chat is **41.3% breached**.

## Business goal
**Reduce completed-ticket first-response breaches from 21.9% to 15.0%.** At roughly **1,768 completed tickets per quarter** and the policy's **Rs350 SLA credit per breach**, this represents approximately **Rs 42,475 lower SLA-credit cost per quarter**, assuming similar volume and channel mix.

## What to investigate
1. Morning chat queue coverage and arrival volume by hour.
2. Whether Morning inherits overnight/previous-shift work.
3. Persistent weekly agent patterns, using both breach rate and ticket count.

## Decisions
UTC was converted to IST before roster matching. Duplicate IDs were treated as migration re-imports and the helpdesk copy retained. Exactly-on-target responses are not breaches.

The email says about forty IVR transcripts failed, but no structured field identifies them, so they were not silently excluded. If Vireo supplies an authoritative failed-IVR list, rerun and document the delta.

The June roster reshuffle is not treated as causal because the post-change window is too short.
