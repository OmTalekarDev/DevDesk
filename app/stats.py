from .database import get_connection


def productivity_stats(user_id: int) -> dict:
    with get_connection() as connection:
        total = connection.execute("SELECT COUNT(*) AS n FROM tasks WHERE user_id = ?", (user_id,)).fetchone()["n"]
        completed = connection.execute("SELECT COUNT(*) AS n FROM tasks WHERE user_id = ? AND completed = 1", (user_id,)).fetchone()["n"]
        pending = total - completed
        daily = connection.execute("""
            SELECT substr(created_at, 1, 10) AS day, COUNT(*) AS count
            FROM tasks WHERE user_id = ? AND created_at >= datetime('now', '-6 days')
            GROUP BY day ORDER BY day
        """, (user_id,)).fetchall()
    rate = round((completed / total) * 100, 1) if total else 0
    return {"total": total, "completed": completed, "pending": pending, "completion_rate": rate,
            "daily_created": [{"day": r["day"], "count": r["count"]} for r in daily]}
