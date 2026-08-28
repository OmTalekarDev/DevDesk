from .database import get_connection


def create_task(title: str, description: str = "") -> dict:
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO tasks (title, description) VALUES (?, ?)",
            (title, description),
        )
        row = connection.execute(
            "SELECT * FROM tasks WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
        connection.commit()
    return dict(row)


def list_tasks() -> list[dict]:
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM tasks ORDER BY id DESC"
        ).fetchall()
    return [dict(row) for row in rows]


def get_task(task_id: int) -> dict | None:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
    return dict(row) if row else None


def update_task(task_id: int, title=None, description=None, completed=None) -> dict | None:
    current = get_task(task_id)
    if current is None:
        return None

    values = {
        "title": current["title"] if title is None else title,
        "description": current["description"] if description is None else description,
        "completed": current["completed"] if completed is None else int(completed),
    }

    with get_connection() as connection:
        connection.execute(
            "UPDATE tasks SET title = ?, description = ?, completed = ? WHERE id = ?",
            (values["title"], values["description"], values["completed"], task_id),
        )
        row = connection.execute(
            "SELECT * FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        connection.commit()
    return dict(row)


def delete_task(task_id: int) -> bool:
    with get_connection() as connection:
        cursor = connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        connection.commit()
    return cursor.rowcount > 0
