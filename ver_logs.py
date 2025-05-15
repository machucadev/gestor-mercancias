from database.db_manager import get_connection

with get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT id, accion, fecha FROM logs ORDER BY id DESC")
    logs = cursor.fetchall()

for log in logs:
    print(f"[{log[2]}] {log[1]}")
