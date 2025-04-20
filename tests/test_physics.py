# tests/test_physics.py

import pytest
from datetime import date
from lunar_lander.physics import gravita_lunare

def test_gravita_lunare_type_and_range():
    """
    gravita_lunare deve restituire un float compreso fra 1.2 e 2.0 (m/s²).
    """
    g = gravita_lunare(date.today())
    # Controllo tipo
    assert isinstance(g, float)
    # Controllo range
    assert 1.2 <= g <= 2.0

@pytest.mark.parametrize("offset_days", [0, 7, 14, 21])
def test_gravita_variabile(offset_days):
    """
    Verifica che la funzione cambi valore passando date diverse.
    (Assumiamo che non restituisca sempre lo stesso valore.)
    """
    d1 = date.today()
    d2 = d1.replace(day=((d1.day + offset_days - 1) % 28) + 1)
    g1 = gravita_lunare(d1)
    g2 = gravita_lunare(d2)
    # In linea di massima, se offset_days diverso da 0, g1 e g2 non sono sempre uguali
    assert isinstance(g2, float)
    # Non è un test rigoroso astronomico, ma assicura variabilità
    if offset_days != 0:
        assert g1 != pytest.approx(g2)
