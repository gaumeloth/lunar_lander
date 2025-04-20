class Lander:
    def __init__(self, x:float, y:float):
        # posizione e velocità
        self.x, self.y = x, y
        self.vel_x, self.vel_y = 0.0, 0.0

        # fuel & heat
        self.fuel:int = 100         # massimo 100 unità
        self.heat = 0.0             # 0-100%
        self.heat_rate = 20.0       # heat per secondo di thrust
        self.cool_rate = 10.0       # heat dissipation per secondo di non-thrust

        # stato motore
        self.engine_enabled = True

    def apply_thrust(self, thrust:float, dt:float):
        """
        Applica un “thrust” di intensità `thrust` (m/s²) per `dt` secondi,
        diminuendo carburante e aumentando heat.
        """
        
        if not self.engine_enabled or self.fuel <= 0.0:
            return

        # Consumo carburante
        self.fuel -= thrust * dt
        if self.fuel < 0.0:
            self.fuel = 0.0

        # Modifica velocità verso l'alto
        self.vel_y -= thrust * dt

        # Aumento calore
        self.heat += self.heat_rate * dt
        if self.heat >= 100.0:
            self.heat = 100.0
            self.engine_enabled = False  # surriscaldamento

    def cool_down(self, dt: float):
        """
        Raffredda il modulo quando non si usa il motore.
        Riduce il calore e, se arriva a zero, riabilita il motore.
        """
        self.heat -= self.cool_rate * dt
        if self.heat <= 0.0:
            self.heat = 0.0
            self.engine_enabled = True
