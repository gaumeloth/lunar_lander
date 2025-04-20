# tests/test_lander.py

import pytest
from lunar_lander.lander import Lander

def test_initial_state():
    """
    Il Lander parte con heat a 0 e motore abilitato.
    """
    lander = Lander(0, 0)
    assert lander.heat == 0.0
    assert lander.engine_enabled is True

def test_heat_buildup_and_engine_disable():
    """
    Applicando thrust abbastanza a lungo, heat arriva a 100 e motore si disabilita.
    """
    lander = Lander(0, 0)
    # dt tale per portare heat = heat_rate * dt = 100 → dt = 100/heat_rate
    dt = 100.0 / lander.heat_rate
    lander.apply_thrust(thrust=10.0, dt=dt)
    assert pytest.approx(lander.heat, abs=1e-6) == 100.0
    assert lander.engine_enabled is False

def test_cooldown_reenables_engine_and_limits_heat():
    """
    Raffreddando a sufficienza, heat torna a 0 e motore si riabilita.
    """
    lander = Lander(0, 0)
    # Simulo surriscaldamento
    lander.heat = 100.0
    lander.engine_enabled = False

    # dt per portare heat a 0 → dt = heat / cool_rate
    dt = lander.heat / lander.cool_rate
    lander.cool_down(dt=dt)
    assert lander.heat == 0.0
    assert lander.engine_enabled is True

def test_heat_bounds_during_cooldown():
    """
    Cool down non deve far andare heat sotto zero.
    """
    lander = Lander(0, 0)
    lander.heat = 10.0
    # raffreddamento maggiore del necessario
    lander.cool_down(dt=5.0)
    assert lander.heat == 0.0

def test_no_thrust_when_engine_disabled_or_no_fuel():
    """
    Se motore disabilitato o carburante a 0, apply_thrust non altera heat né fuel.
    """
    # Caso motore disabilitato
    lander = Lander(0, 0)
    lander.engine_enabled = False
    initial_heat = lander.heat
    initial_fuel = lander.fuel
    lander.apply_thrust(thrust=10.0, dt=1.0)
    assert lander.heat == initial_heat
    assert lander.fuel == initial_fuel

    # Caso carburante esaurito
    lander = Lander(0, 0)
    lander.fuel = 0.0
    lander.heat = 0.0
    lander.apply_thrust(thrust=10.0, dt=1.0)
    assert lander.heat == 0.0
    assert lander.fuel == 0.0
