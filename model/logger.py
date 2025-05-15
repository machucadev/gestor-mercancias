from model.observer import Observer

class Logger:
    def __init__(self):
        self.observadores = []

    def registrar_observador(self, obs: Observer):
        self.observadores.append(obs)

    def notificar_observadores(self, mensaje: str):
        for obs in self.observadores:
            obs.actualizar(mensaje)
