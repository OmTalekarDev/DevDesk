from .database import get_connection


def create_task(title: str, description: str = "", user_id: int | None = None) -> dict:
    with get_connection() as connection:
        cursor = connection.execute("INSERT INTO tasks (title, description, user_id) VALUES (?, ?, ?)", (title, description, user_id))
        row = connection.execute("SELECT * FROM tasks WHERE id = ?", (cursor.lastrowid,)).fetchone()
        connection.commit()
    return dict(row)


def list_tasks(user_id: int) -> list[dict]:
    with get_connection() as connection:
        rows = connection.execute("SELECT * FROM tasks WHERE user_id = ? ORDER BY id DESC", (user_id,)).fetchall()
    return [dict(row) for row in rows]


def get_task(task_id: int, user_id: int) -> dict | None:
    with get_connection() as connection:
        row = connection.execute("SELECT * FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id)).fetchone()
    return dict(row) if row else None


def update_task(task_id: int, user_id: int, title=None, description=None, completed=None) -> dict | None:
    current = get_task(task_id, user_id)
    if current is None:
        return None
    values = {"title": current["title"] if title is None else title,
              "description": current["description"] if description is None else description,
              "completed": current["completed"] if completed is None else int(completed)}
    with get_connection() as connection:
        connection.execute("UPDATE tasks SET title = ?, description = ?, completed = ? WHERE id = ? AND user_id = ?",
                           (values["title"], values["description"], values["completed"], task_id, user_id))
        row = connection.execute("SELECT * FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id)).fetchone()
        connection.commit()
    return dict(row)


def delete_task(task_id: int, user_id: int) -> bool:
    with get_connection() as connection:
        cursor = connection.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
        connection.commit()
    return cursor.rowcount > 0
