# tests/test_lander.py

import pytest
from datetime import date
from lunar_lander.lander import Lander
from lunar_lander.events import Event

def test_initial_state():
    """
    Il Lander parte con:
    - heat a 0
    - motore abilitato
    - fuel a 100
    - nessun evento attivo (active_event is None)
    - event_end_time a 0.0
    """
    lander = Lander(0, 0)
    assert lander.heat == 0.0
    assert lander.engine_enabled is True
    assert lander.fuel == 100.0
    assert lander.active_event is None
    assert lander.event_end_time == 0.0

def test_heat_buildup_and_engine_disable():
    """
    Applicando thrust abbastanza a lungo:
    - heat → 100
    - motore disabilitato
    - fuel diminuisce
    """
    lander = Lander(0, 0)
    dt = 100.0 / lander.heat_rate
    initial_fuel = lander.fuel
    lander.apply_thrust(thrust=10.0, dt=dt)
    assert pytest.approx(lander.heat, abs=1e-6) == 100.0
    assert lander.engine_enabled is False
    assert lander.fuel < initial_fuel

def test_cooldown_reenables_engine_and_limits_heat():
    """
    Raffreddando a sufficienza:
    - heat → 0
    - motore riabilitato
    """
    lander = Lander(0, 0)
    lander.heat = 100.0
    lander.engine_enabled = False
    dt = lander.heat / lander.cool_rate
    lander.cool_down(dt=dt)
    assert lander.heat == 0.0
    assert lander.engine_enabled is True

def test_heat_bounds_during_cooldown():
    """
    Cool down non deve far scendere heat sotto 0.
    """
    lander = Lander(0, 0)
    lander.heat = 10.0
    lander.cool_down(dt=5.0)
    assert lander.heat == 0.0

def test_no_thrust_when_engine_disabled_or_no_fuel():
    """
    Se motore disabilitato o carburante esaurito,
    apply_thrust non altera né heat né fuel.
    """
    # motore disabilitato
    lander = Lander(0, 0)
    h0, f0 = lander.heat, lander.fuel
    lander.engine_enabled = False
    lander.apply_thrust(thrust=10.0, dt=1.0)
    assert lander.heat == h0
    assert lander.fuel == f0

    # carburante esaurito
    lander = Lander(0, 0)
    lander.fuel = 0.0
    h0, f0 = lander.heat, lander.fuel
    lander.apply_thrust(thrust=10.0, dt=1.0)
    assert lander.heat == h0
    assert lander.fuel == f0

def test_simulate_event_default_behavior():
    """
    simulate_event(current_time) di default non scatena eventi
    e lascia active_event a None.
    """
    lander = Lander(0, 0)
    # Disabilito tutte le probabilità per rendere il test deterministico
    lander.event_manager.base_probs= {'meteorite':0.0, 'tempesta': 0.0}
    ev = lander.simulate_event(current_time=0.0)
    assert ev is None
    assert lander.active_event is None

def test_simulate_event_sets_active_event():
    """
    Forzando EventManager.base_probs, simulate_event deve ritornare
    un Event e popolare active_event e event_end_time.
    """
    lander = Lander(0, 0)
    # Forzo sempre meteorite
    lander.event_manager.base_probs = {'meteorite': 1.0, 'tempesta': 0.0}
    t = 5.0
    ev = lander.simulate_event(current_time=t)
    assert isinstance(ev, Event)
    assert lander.active_event is ev
    assert ev.name == 'meteorite'
    # event_end_time deve essere t + ev.duration (duration = 0 per meteorite)
    assert lander.event_end_time == pytest.approx(t + ev.duration)
