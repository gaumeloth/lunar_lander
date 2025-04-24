# tests/test_event.py

import pytest
import random
from lunar_lander.events import EventManager, Event

@pytest.fixture(autouse=True)
def seed_random():
    # Ensure reproducible tests
    random.seed(0)
    yield
    random.seed()

def test_eventmanager_defaults():
    """
    Verifica che EventManager abbia attributi di default corretti.
    """
    em = EventManager()
    assert hasattr(em, 'cooldown')
    assert isinstance(em.cooldown, float)
    # Probabilità base configurate
    assert 'meteorite' in em.base_probs
    assert 'tempesta' in em.base_probs

def test_cooldown_prevents_events():
    """
    Con cooldown > 0, un secondo evento consecutivo non scatta.
    """
    em = EventManager(cooldown=5.0)
    # Primo evento possibile
    ev1 = em.maybe_trigger(current_time=0.0)
    if ev1 is None:
        pytest.skip("EventManager didn't trigger any event on first call; adjust base_probs for test.")
    # Secondo tentativo entro il cooldown
    ev2 = em.maybe_trigger(current_time=em.cooldown / 2)
    assert ev2 is None

def test_event_generation_meteorite():
    """
    Forza la generazione di un meteorite impostando base_probs,
    e verifica proprietà dell'Event.
    """
    em = EventManager(cooldown=0.0)
    em.base_probs = {'meteorite': 1.0, 'tempesta': 0.0}
    t = 10.0
    ev = em.maybe_trigger(current_time=t)
    assert isinstance(ev, Event)
    assert ev.name == 'meteorite'
    # severity dovrebbe essere in 0.1–0.5 e duration 0
    assert 0.1 <= ev.severity <= 0.5
    assert ev.duration == 0.0
    assert ev.timestamp == t

def test_event_generation_tempesta():
    """
    Forza la generazione di una tempesta impostando base_probs,
    e verifica proprietà dell'Event.
    """
    em = EventManager(cooldown=0.0)
    em.base_probs = {'meteorite': 0.0, 'tempesta': 1.0}
    t = 20.0
    ev = em.maybe_trigger(current_time=t)
    assert isinstance(ev, Event)
    assert ev.name == 'tempesta'
    # severity in 0.5–1.0, duration in 2.0–5.0
    assert 0.5 <= ev.severity <= 1.0
    assert 2.0 <= ev.duration <= 5.0
    assert ev.timestamp == t

def test_no_event_when_within_active_duration():
    """
    Se un evento è ancora in corso (basato su timestamp+duration),
    EventManager non deve generarne uno nuovo.
    """
    em = EventManager(cooldown=0.0)
    # Forzo un evento con durata 3
    ev = Event(name='tempesta', severity=0.7, duration=3.0, timestamp=5.0)
    em.last_event_time = ev.timestamp
    em.last_event_duration = ev.duration
    em.base_probs = {'tempesta': 1.0, 'meteorite': 0.0}
    # current_time < timestamp + duration
    new_ev = em.maybe_trigger(current_time=ev.timestamp + ev.duration / 2)
    assert new_ev is None
