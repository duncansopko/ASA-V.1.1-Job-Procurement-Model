print("CLI FILE EXECUTING")
import argparse

from scripts.score_applications import (
    add_application,
    add_customization,
    add_outreach,
)

# ==================================================
# Command Handlers
# ==================================================

def add_application_cmd(args):
    application_id = add_application(
        company=args.company,
        role=args.role,
        application_link=args.link,
    )

    if args.resume_customized or args.cover_letter_customized:
        add_customization(
            application_id=application_id,
            resume_customized=args.resume_customized,
            cover_letter_customized=args.cover_letter_customized,
        )

    print(f"Application {application_id} added successfully.")


def outreach_cmd(args):
    add_outreach(
        application_id=args.application_id,
        channel=args.channel,
        outreach_type=args.type,
    )

import argparse

from scripts.score_applications import (
    add_application,
    add_customization,
    add_outreach,
)

def add_application_cmd(args):
    application_id = add_application(
        company=args.company,
        role=args.role,
        application_link=args.link,
    )

    if args.resume_customized or args.cover_letter_customized:
        add_customization(
            application_id=application_id,
            resume_customized=args.resume_customized,
            cover_letter_customized=args.cover_letter_customized,
        )

    print(f"Application {application_id} added successfully.")

def outreach_cmd(args):
    add_outreach(
        application_id=args.application_id,
        channel=args.channel,
        outreach_type=args.type,
    )

    print(
        f"Outreach logged for application {args.application_id} via {args.channel}."
    )

def main():
    parser = argparse.ArgumentParser(
        description="ASA v1.1 — Job Application CLI"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    # --------------------
    # add application
    # --------------------
    add_parser = subparsers.add_parser(
        "add", help="Add a new application"
    )

    add_parser.add_argument("--company", required=True)
    add_parser.add_argument("--role", required=True)
    add_parser.add_argument("--link")
    add_parser.add_argument("--resume-customized", action="store_true")
    add_parser.add_argument("--cover-letter-customized", action="store_true")

    add_parser.set_defaults(func=add_application_cmd)

    # --------------------
    # outreach
    # --------------------
    outreach_parser = subparsers.add_parser(
        "outreach", help="Log outreach activity"
    )

    outreach_parser.add_argument(
        "--application-id", type=int, required=True
    )
    outreach_parser.add_argument(
        "--channel", required=True
    )
    outreach_parser.add_argument(
        "--type",
        choices=["initial", "follow_up"],
        default="initial",
        help="Type of outreach"
    )

    outreach_parser.set_defaults(func=outreach_cmd)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()

