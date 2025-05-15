import socket
from database.db_manager import get_connection

HOST = 'localhost'
PORT = 8082

def guardar_log_en_bd(mensaje):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO logs (accion, fecha) VALUES (?, datetime('now'))", (mensaje,))
        conn.commit()

def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Servidor de logs escuchando en {HOST}:{PORT}")

        while True:
            cliente_socket, addr = server_socket.accept()
            with cliente_socket:
                print(f"Conexión desde {addr}")
                data = cliente_socket.recv(1024)
                if data:
                    mensaje = data.decode('utf-8')
                    print(f"Log recibido: {mensaje}")
                    guardar_log_en_bd(mensaje)

if __name__ == "__main__":
    iniciar_servidor()
