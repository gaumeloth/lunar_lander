#!/usr/bin/env python3
from lunar_lander.physics import gravita_lunare
from datetime import date

if __name__ == "__main__":
    g = gravita_lunare(date.today())
    print(f"g oggi: {g:.3f} m/s²")
