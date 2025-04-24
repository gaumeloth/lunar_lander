import random
from typing import NamedTuple, Optional, List

class Event(NamedTuple):
    name: str               # 'meteorite' o 'tempesta'
    severity: float         # intensità (0.0–1.0)
    duration: float         # in secondi (solo per tempesta)
    timestamp: float        # momento di trigger del gioco

class EventManager:
    """
    Tiene traccia degli eventi già lanciati e decide se e quale
    evento scatenare in ogni tick del gioco.
    """
    def __init__(self, cooldown:float = 5.0):
        self.cooldown = cooldown                # tempo minimo fra due eventi
        self.last_event_time:float = -cooldown  # tempo rimanente per prossimo possibile evento
        self.last_event_duration:float = 0.0    # durata ultimo evento

        self.base_probs = {                     # probabilità base per evento
            'meteorite': 0.01,
            'tempesta': 0.005
        }

    def maybe_trigger(self, current_time: float) -> Optional[Event]:
        """
        Prova a generare un evento se è passato almeno `cooldown`
        dal precedente. Ritorna l’Event o None.
        """
        # Se un evento è ancora in corso (durata residua), non lanciare
        if current_time < self.last_event_time + self.last_event_duration:
            return None

        # Rispetta anche il cooldown tra eventi
        if current_time - self.last_event_time < self.cooldown:
            return None

        # Scegli evento in base alle probabilità cumulative
        r = random.random()
        cum_prob = 0.0
        for name, prob in self.base_probs.items():
            cum_prob += prob
            if r < cum_prob:
                ev = self._make_event(name, current_time)
                # Registra timestamp e durata per il prossimo controllo
                self.last_event_time = current_time
                self.last_event_duration=ev.duration
                return ev
        return None

    def _make_event(self, name: str, t: float) -> Event:
        # crea l'istanza di Event con severity e duration a caso
        if name == 'meteorite':
            severity = random.uniform(0.1, 0.5)  # impatto leggero→medio
            duration = 0.0
            return Event(name, severity, duration=0.0, timestamp=t)
        else:  # 'tempesta'
            severity = random.uniform(0.5, 1.0)  # tempesta media→forte
            duration = random.uniform(2.0, 5.0)   # secondi
        return Event(name=name, severity=severity, duration=duration, timestamp=t)
