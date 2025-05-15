import socket

HOST = 'localhost'
PORT = 8082

def enviar_log(mensaje):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(mensaje.encode('utf-8'))
    except Exception as e:
        print(f"No se pudo enviar el log al servidor: {e}")
