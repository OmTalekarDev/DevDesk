from .database import get_connection


def productivity_stats() -> dict:
    with get_connection() as connection:
        total = connection.execute("SELECT COUNT(*) AS n FROM tasks").fetchone()["n"]
        completed = connection.execute("SELECT COUNT(*) AS n FROM tasks WHERE completed = 1").fetchone()["n"]
        pending = total - completed
        daily = connection.execute("""
            SELECT substr(created_at, 1, 10) AS day, COUNT(*) AS count
            FROM tasks
            WHERE created_at >= datetime('now', '-6 days')
            GROUP BY day ORDER BY day
        """).fetchall()
    rate = round((completed / total) * 100, 1) if total else 0
    return {"total": total, "completed": completed, "pending": pending, "completion_rate": rate,
            "daily_created": [{"day": r["day"], "count": r["count"]} for r in daily]}
