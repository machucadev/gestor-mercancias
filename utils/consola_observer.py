from model.observer import Observer

class ConsolaObserver(Observer):
    def actualizar(self, mensaje: str):
        print(f"[OBSERVADOR] {mensaje}")
