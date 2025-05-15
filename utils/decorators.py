from datetime import datetime
from database.db_manager import get_connection
from server.log_client import enviar_log
from utils.sesion import usuario_actual

def log_action(action_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            mensaje_log = f"[{fecha}] {usuario_actual} realizó: {action_name}"

            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO logs (accion, fecha) VALUES (?, ?)",
                    (mensaje_log, fecha)
                )
                conn.commit()

            enviar_log(mensaje_log)
            return result
        return wrapper
    return decorator
