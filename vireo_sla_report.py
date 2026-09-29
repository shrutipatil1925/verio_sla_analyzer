import argparse
import json
from pathlib import Path

import pandas as pd


TARGET_MIN = {
    "chat": 15,
    "voice": 120,
    "social": 240,
    "email": 480,
}

SLA_CREDIT = 350
IST = "Asia/Kolkata"


def run(data_dir="data", out_dir="outputs"):
    data_path = Path(data_dir)
    output_path = Path(out_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------
    # 1. Load data
    # ---------------------------------------------------------
    tickets = pd.read_csv(data_path / "tickets.csv")
    agents = pd.read_csv(data_path / "agents.csv")

    raw_rows = len(tickets)

    # ---------------------------------------------------------
    # 2. Parse timestamps
    # ---------------------------------------------------------
    for column in ["created_at", "first_response_at", "resolved_at"]:
        tickets[column] = pd.to_datetime(
            tickets[column],
            utc=True,
            errors="coerce",
        )

    agents["from_date"] = pd.to_datetime(
        agents["from_date"],
        errors="coerce",
    )

    agents["to_date"] = pd.to_datetime(
        agents["to_date"],
        errors="coerce",
    )

    # ---------------------------------------------------------
    # 3. Basic input validation
    # ---------------------------------------------------------
    missing_created = int(tickets["created_at"].isna().sum())
    missing_response = int(tickets["first_response_at"].isna().sum())
    missing_agent = int(tickets["agent_id"].isna().sum())

    # ---------------------------------------------------------
    # 4. Remove migration duplicates
    #
    # If the same ticket_id exists in both systems,
    # prefer the helpdesk copy.
    # ---------------------------------------------------------
    tickets["_helpdesk_priority"] = (
        tickets["source_system"].eq("helpdesk").astype(int)
    )

    tickets = (
        tickets.sort_values(["ticket_id", "_helpdesk_priority"])
        .drop_duplicates("ticket_id", keep="last")
        .drop(columns="_helpdesk_priority")
        .reset_index(drop=True)
    )

    duplicate_rows_removed = raw_rows - len(tickets)

    # ---------------------------------------------------------
    # 5. Convert timestamps to IST
    # ---------------------------------------------------------
    tickets["created_ist"] = tickets["created_at"].dt.tz_convert(IST)

    tickets["response_ist"] = tickets["first_response_at"].dt.tz_convert(IST)

    # ---------------------------------------------------------
    # 6. Calculate response time and SLA target
    # ---------------------------------------------------------
    tickets["response_minutes"] = (
        tickets["first_response_at"] - tickets["created_at"]
    ).dt.total_seconds() / 60

    tickets["target_minutes"] = tickets["channel"].map(TARGET_MIN)

    # ---------------------------------------------------------
    # 7. SLA breach
    #
    # A breach means the first response was later than
    # the channel-specific target.
    # ---------------------------------------------------------
    tickets["breach"] = (
        tickets["first_response_at"].notna()
        & tickets["target_minutes"].notna()
        & (tickets["response_minutes"] > tickets["target_minutes"])
    )

    tickets["completed"] = tickets["status"].isin(
        ["resolved", "closed"]
    )

    tickets["sla_credit"] = (
        tickets["breach"].astype(int) * SLA_CREDIT
    )

    # ---------------------------------------------------------
    # 8. Assign agent roster information
    #
    # Assignment is based on the date of first response.
    # ---------------------------------------------------------
    attributes = []

    for _, row in tickets.iterrows():

        response_date = row["response_ist"].date()

        roster_rows = agents[
            (agents["agent_id"] == row["agent_id"])
            & (
                agents["from_date"].dt.date
                <= response_date
            )
            & (
                agents["to_date"]
                .fillna(pd.Timestamp("2099-12-31"))
                .dt.date
                >= response_date
            )
        ]

        if len(roster_rows) == 1:
            agent = roster_rows.iloc[0]

            attributes.append(
                (
                    agent["name"],
                    agent["site"],
                    agent["team"],
                    int(agent["tier"]),
                    agent["shift"],
                )
            )
        else:
            attributes.append(
                (
                    None,
                    None,
                    None,
                    None,
                    None,
                )
            )

    tickets[
        [
            "agent_name",
            "site",
            "team",
            "tier",
            "shift_name",
        ]
    ] = pd.DataFrame(
        attributes,
        index=tickets.index,
    )

    # ---------------------------------------------------------
    # 9. Weekly reporting in IST
    # ---------------------------------------------------------
    tickets["week_start_ist"] = (
        tickets["created_ist"].dt.normalize()
        - pd.to_timedelta(
            tickets["created_ist"].dt.weekday,
            unit="D",
        )
    ).dt.strftime("%Y-%m-%d")

    # ---------------------------------------------------------
    # 10. Report tables
    # ---------------------------------------------------------

    weekly_summary = (
        tickets.groupby(
            "week_start_ist",
            as_index=False,
        )
        .agg(
            tickets=("ticket_id", "size"),
            breaches=("breach", "sum"),
            breach_rate=("breach", "mean"),
            sla_credit_exposure=("sla_credit", "sum"),
        )
    )

    weekly_agent_shift = (
        tickets.groupby(
            [
                "week_start_ist",
                "agent_id",
                "agent_name",
                "site",
                "team",
                "tier",
                "shift_name",
            ],
            as_index=False,
        )
        .agg(
            tickets=("ticket_id", "size"),
            breaches=("breach", "sum"),
            breach_rate=("breach", "mean"),
            sla_credit_exposure=("sla_credit", "sum"),
        )
    )

    weekly_shift = (
        tickets.groupby(
            [
                "week_start_ist",
                "shift_name",
            ],
            as_index=False,
        )
        .agg(
            tickets=("ticket_id", "size"),
            breaches=("breach", "sum"),
            breach_rate=("breach", "mean"),
            sla_credit_exposure=("sla_credit", "sum"),
        )
    )

    agent_summary = (
        tickets.groupby(
            [
                "agent_id",
                "agent_name",
                "site",
                "team",
                "tier",
                "shift_name",
            ],
            as_index=False,
        )
        .agg(
            tickets=("ticket_id", "size"),
            breaches=("breach", "sum"),
            breach_rate=("breach", "mean"),
            sla_credit_exposure=("sla_credit", "sum"),
        )
    )

    channel_shift_summary = (
        tickets.groupby(
            [
                "shift_name",
                "channel",
            ],
            as_index=False,
        )
        .agg(
            tickets=("ticket_id", "size"),
            breaches=("breach", "sum"),
            breach_rate=("breach", "mean"),
            sla_credit_exposure=("sla_credit", "sum"),
        )
    )

    # ---------------------------------------------------------
    # 11. Overall summary
    # ---------------------------------------------------------
    total_tickets = len(tickets)

    total_breaches = int(tickets["breach"].sum())

    completed = tickets[tickets["completed"]]

    open_pending = tickets[
        ~tickets["completed"]
    ]

    completed_tickets = len(completed)

    completed_breaches = int(
        completed["breach"].sum()
    )

    open_pending_tickets = len(open_pending)

    open_pending_breaches = int(
        open_pending["breach"].sum()
    )

    overall_summary = pd.DataFrame(
        [
            {
                "metric": "raw_ticket_rows",
                "value": raw_rows,
            },
            {
                "metric": "unique_tickets_after_dedupe",
                "value": total_tickets,
            },
            {
                "metric": "duplicate_rows_removed",
                "value": duplicate_rows_removed,
            },
            {
                "metric": "total_breaches",
                "value": total_breaches,
            },
            {
                "metric": "overall_breach_rate_percent",
                "value": round(
                    tickets["breach"].mean() * 100,
                    2,
                ),
            },
            {
                "metric": "completed_tickets",
                "value": completed_tickets,
            },
            {
                "metric": "completed_breaches",
                "value": completed_breaches,
            },
            {
                "metric": "completed_breach_rate_percent",
                "value": round(
                    completed["breach"].mean() * 100,
                    2,
                ),
            },
            {
                "metric": "completed_sla_credit_exposure_inr",
                "value": completed_breaches * SLA_CREDIT,
            },
            {
                "metric": "open_pending_tickets",
                "value": open_pending_tickets,
            },
            {
                "metric": "open_pending_breaches",
                "value": open_pending_breaches,
            },
            {
                "metric": "open_pending_breach_rate_percent",
                "value": round(
                    open_pending["breach"].mean() * 100,
                    2,
                ),
            },
            {
                "metric": "all_ticket_sla_credit_exposure_inr",
                "value": total_breaches * SLA_CREDIT,
            },
        ]
    )

    # ---------------------------------------------------------
    # 12. QA evidence
    # ---------------------------------------------------------
    qa = {
        "raw_rows": raw_rows,
        "unique_tickets_after_dedupe": total_tickets,
        "duplicate_rows_removed": duplicate_rows_removed,
        "missing_created_at": missing_created,
        "missing_first_response_at": missing_response,
        "missing_agent_id": missing_agent,
        "unique_ticket_ids": bool(tickets["ticket_id"].is_unique),
        "negative_response_intervals": int(
            (tickets["response_minutes"] < 0).sum()
        ),
        "unknown_channel_targets": int(
            tickets["target_minutes"].isna().sum()
        ),
        "unmatched_roster_rows": int(
            tickets["shift_name"].isna().sum()
        ),
        "nonnegative_response": bool(
            (tickets["response_minutes"] >= 0).all()
        ),
        "known_targets": bool(
            tickets["target_minutes"].notna().all()
        ),
        "roster_match": bool(
            tickets["shift_name"].notna().all()
        ),
        "completed_tickets": completed_tickets,
        "completed_breaches": completed_breaches,
        "completed_breach_rate_percent": round(
            completed["breach"].mean() * 100,
            2,
        ),
        "completed_sla_credit_exposure_inr": (
            completed_breaches * SLA_CREDIT
        ),
    }

    # ---------------------------------------------------------
    # 13. Save outputs
    # ---------------------------------------------------------
    outputs = {
        "scored_tickets": tickets,
        "overall_summary": overall_summary,
        "weekly_summary": weekly_summary,
        "weekly_agent_shift": weekly_agent_shift,
        "weekly_shift": weekly_shift,
        "agent_summary": agent_summary,
        "channel_shift_summary": channel_shift_summary,
    }

    for name, dataframe in outputs.items():
        dataframe.to_csv(
            output_path / f"{name}.csv",
            index=False,
        )

    (output_path / "qa_report.json").write_text(
        json.dumps(
            qa,
            indent=2,
        ),
        encoding="utf-8",
    )

    # ---------------------------------------------------------
    # 14. Console summary
    # ---------------------------------------------------------
    print("\nVireo Audio — First-response SLA Report")
    print("-" * 48)
    print(f"Raw rows:                 {raw_rows:,}")
    print(f"Unique tickets:           {total_tickets:,}")
    print(f"Duplicate rows removed:   {duplicate_rows_removed:,}")
    print(f"Total breaches:           {total_breaches:,}")
    print(
        f"Overall breach rate:      "
        f"{tickets['breach'].mean() * 100:.2f}%"
    )
    print()
    print(f"Completed tickets:        {completed_tickets:,}")
    print(f"Completed breaches:       {completed_breaches:,}")
    print(
        f"Completed breach rate:    "
        f"{completed['breach'].mean() * 100:.2f}%"
    )
    print(
        f"Completed credit exposure:"
        f" ₹{completed_breaches * SLA_CREDIT:,.0f}"
    )
    print()
    print(f"Open/pending tickets:      {open_pending_tickets:,}")
    print(f"Open/pending breaches:     {open_pending_breaches:,}")
    print()
    print("QA")
    print(f"Missing first responses:    {missing_response}")
    print(f"Missing agent IDs:          {missing_agent}")
    print(
        f"Negative response times:    "
        f"{qa['negative_response_intervals']}"
    )
    print(
        f"Unmatched roster rows:      "
        f"{qa['unmatched_roster_rows']}"
    )
    print()
    print(f"Outputs written to:         {output_path.resolve()}")
    print("-" * 48)

    return tickets


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Vireo Audio first-response SLA report"
    )

    parser.add_argument(
        "--data",
        default="data",
        help="Input data directory",
    )

    parser.add_argument(
        "--out",
        default="outputs",
        help="Output directory",
    )

    args = parser.parse_args()

    run(
        data_dir=args.data,
        out_dir=args.out,
    )

