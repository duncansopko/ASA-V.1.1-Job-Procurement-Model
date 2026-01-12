import sqlite3
from pathlib import Path
from datetime import datetime, timezone

# Database path
DB_PATH = Path(__file__).resolve().parents[1] / "data" / "asa.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


# -------------------------
# Per-application metrics
# -------------------------

def total_outreach_count(application_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM outreach_events
        WHERE application_id = ?
        """,
        (application_id,)
    )

    count = cursor.fetchone()[0]
    conn.close()
    return count


def follow_up_count(application_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM outreach_events
        WHERE application_id = ?
          AND outreach_type = 'follow_up'
        """,
        (application_id,)
    )

    count = cursor.fetchone()[0]
    conn.close()
    return count


def total_action_count(application_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*) FROM status_history
        WHERE application_id = ?
        """,
        (application_id,)
    )
    status_count = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*) FROM outreach_events
        WHERE application_id = ?
        """,
        (application_id,)
    )
    outreach_count = cursor.fetchone()[0]

    conn.close()
    return status_count + outreach_count


def has_follow_up(application_id):
    return follow_up_count(application_id) >= 1


def effort_score_raw(application_id):
    # v1.1 definition: simple count of actions
    return total_action_count(application_id)

def days_since_last_action(application_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT MAX(ts) FROM (
            SELECT timestamp AS ts FROM status_history WHERE application_id = ?
            UNION ALL
            SELECT timestamp AS ts FROM outreach_events WHERE application_id = ?
            UNION ALL
            SELECT created_at AS ts FROM applications WHERE application_id = ?
        )
        """,
        (application_id, application_id, application_id)
    )

    result = cursor.fetchone()[0]
    conn.close()

    if result is None:
        return None

    last_action_time = datetime.fromisoformat(result)
    now = datetime.now(timezone.utc)

    # ensure both are timezone-aware
    if last_action_time.tzinfo is None:
        last_action_time = last_action_time.replace(tzinfo=timezone.utc)

    return (now - last_action_time).days


def current_status(application_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT status
        FROM status_history
        WHERE application_id = ?
        ORDER BY timestamp DESC
        LIMIT 1
        """,
        (application_id,)
    )

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    return row[0]

# -------------------------
# Application metrics view
# -------------------------

def application_metrics_view():
    """
    Returns one row per application with core behavioral metrics.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT application_id
        FROM applications
        """
    )

    application_ids = [row[0] for row in cursor.fetchall()]
    conn.close()

    rows = []

    for app_id in application_ids:
        row = {
            "application_id": app_id,
            "current_status": current_status(app_id),
            "days_since_last_action": days_since_last_action(app_id),
            "total_outreach_count": total_outreach_count(app_id),
            "follow_up_count": follow_up_count(app_id),
            "has_follow_up": has_follow_up(app_id),
            "total_action_count": total_action_count(app_id),
            "effort_score_raw": effort_score_raw(app_id),
        }
        rows.append(row)

    return rows


# -------------------------
# Test harness
# -------------------------

if __name__ == "__main__":
    print("Running application metrics view...\n")

    metrics = application_metrics_view()
    for row in metrics:
        print(row)

