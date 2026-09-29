# AI Prompts Used

## AI tools used

* ChatGPT — used during development and review.
* No paid AI API call is used by the submitted runtime tool.
* The final SLA calculations are deterministic Python calculations using the supplied data and support policy.

## Prompt 1 — Manager summary

> Using only supplied aggregate SLA statistics, write a concise factual manager summary. Do not infer unsupported causes. Mention uncertainty and the Tier 2 caveat. Give 3 observations and 3 investigation questions. Do not change numbers.

**Used for:** Structuring the manager memo and identifying factual observations/investigation questions.

## Prompt 2 — QA challenge

> Act as a skeptical data-quality reviewer. Identify only checks that could invalidate the SLA calculation: timezone, migration duplicates, roster effective dates, channel targets, missing responses, and exact-target boundary handling. Do not invent data.

**Used for:** Reviewing data-quality risks and making the validation checks explicit.

## Other AI-assisted development

AI was also used to:

* review the Python reporting logic;
* identify edge cases in the SLA calculation;
* review assumptions and unsupported conclusions;
* help structure the README and documentation.

## What was changed or discarded

During development, some conclusions were deliberately removed or narrowed when they were not supported by the supplied evidence. In particular:

* An unsupported 15% breach-rate target was removed.
* Unsupported causal claims about the June roster reshuffle were removed.
* Customer/order/product joins were not included because they were not required for the SLA analysis.
* Failed-IVR cases were not silently excluded because the supplied structured data did not provide a reliable way to identify them.

## Final approach

AI assisted with development, review, and documentation. The submitted runtime report does **not** depend on an LLM to calculate SLA breaches. The final calculations use deterministic rules from the support policy, making the results reproducible.
