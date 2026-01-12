import argparse

from score_applications import (
    add_application,
    add_customization,
)

def main():
    parser = argparse.ArgumentParser(
        description="ASA v1.1 — Job Application CLI"
    )

    parser.add_argument(
        "--company",
        required=True,
        help="Company name"
    )

    parser.add_argument(
        "--role",
        required=True,
        help="Role title"
    )

    parser.add_argument(
        "--link",
        help="Application link (optional)"
    )

    parser.add_argument(
        "--resume-customized",
        action="store_true",
        help="Resume was customized for this application"
    )

    parser.add_argument(
        "--cover-letter-customized",
        action="store_true",
        help="Cover letter was customized for this application"
    )

    args = parser.parse_args()

    # ---- Create application ----
    application_id = add_application(
        company=args.company,
        role=args.role,
        application_link=args.link,
    )

    # ---- Log customization (behavioral only) ----
    if args.resume_customized or args.cover_letter_customized:
        add_customization(
            application_id=application_id,
            resume_customized=args.resume_customized,
            cover_letter_customized=args.cover_letter_customized,
        )

    print(f"Application {application_id} added successfully.")

if __name__ == "__main__":
    main()

