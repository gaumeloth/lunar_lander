# lunar_lander/lander.py
import random
from typing import Optional
from lunar_lander.events import Event, EventManager

class Lander:
    """
    Classe che rappresenta il modulo lunare con gestione di posizione, velocità,
    carburante, calore ed eventi casuali.
    """
    def __init__(self, x: float, y: float):
        # Posizione e velocità
        self.x, self.y = x, y
        self.vel_x, self.vel_y = 0.0, 0.0

        # Fuel & Heat
        self.fuel = 100.0       # massimo 100 unità
        self.heat = 0.0         # range 0–100%
        self.heat_rate = 20.0   # heat per secondo di thrust
        self.cool_rate = 10.0   # dissipazione heat per secondo senza thrust

        # Stato motore
        self.engine_enabled = True

        # Eventi casuali
        self.event_manager = EventManager(cooldown=10.0)
        self.active_event: Optional[Event] = None
        self.event_end_time: float = 0.0

    def apply_thrust(self, thrust: float, dt: float):
        """
        Applica un thrust di intensità `thrust` (m/s²) per `dt` secondi,
        diminuendo carburante e aumentando il calore.
        Se il motore è disabilitato o non c'è carburante, non fa nulla.
        """
        if not self.engine_enabled or self.fuel <= 0.0:
            return

        # Consumo carburante
        self.fuel -= thrust * dt
        if self.fuel < 0.0:
            self.fuel = 0.0

        # Modifica velocità verso l'alto
        self.vel_y -= thrust * dt

        # Increase heat
        self.heat += self.heat_rate * dt
        if self.heat >= 100.0:
            self.heat = 100.0
            self.engine_enabled = False  # motore disabilitato per surriscaldamento

    def cool_down(self, dt: float):
        """
        Raffredda il modulo quando non si usa il motore.
        Riduce il calore e, se arriva a zero, riabilita il motore.
        """
        self.heat -= self.cool_rate * dt
        if self.heat <= 0.0:
            self.heat = 0.0
            self.engine_enabled = True

    def simulate_event(self, current_time: float) -> Optional[Event]:
        """
        Gestisce la logica di lancio degli eventi casuali:
        - Non lancia nuovi eventi se uno è ancora in corso.
        - Utilizza EventManager per cooldown e probabilità.
        Ritorna l'oggetto Event creato o None.
        """
        # Se un evento è ancora attivo, non lanciare nulla
        if self.active_event and current_time < self.event_end_time:
            return None

        # Prova a scatenare un nuovo evento
        event = self.event_manager.maybe_trigger(current_time)
        if event:
            self.active_event = event
            self.event_end_time = current_time + event.duration
        return event
