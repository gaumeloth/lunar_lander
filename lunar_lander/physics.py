import ephem
from datetime import date

def gravita_lunare(data: date = date.today()) -> float:
    luna = ephem.Moon(data)
    fase = luna.phase  # 0.0–100.0
    g_min, g_max = 1.2, 2.0
    return g_min + (fase/100.0)*(g_max-g_min)

