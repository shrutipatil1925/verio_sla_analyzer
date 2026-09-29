# AI prompts used

Manager summary:
> Using only supplied aggregate SLA statistics, write a concise factual manager summary. Do not infer unsupported causes. Mention uncertainty and the Tier 2 caveat. Give 3 observations and 3 investigation questions. Do not change numbers.

QA challenge:
> Act as a skeptical data-quality reviewer. Identify only checks that could invalidate the SLA calculation: timezone, migration duplicates, roster effective dates, channel targets, missing responses, and exact-target boundary handling. Do not invent data.

AI was used for summarization/challenge; deterministic code calculated the report.
