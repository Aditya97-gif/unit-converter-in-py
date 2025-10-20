from typing import Dict, List
import sys
import math
import datetime

_UNIT_MAPS: Dict[str, Dict[str, float]] = {
    "length": {  # base: meter
        "m": 1.0, "meter": 1.0, "meters": 1.0,
        "mm": 0.001, "millimeter": 0.001, "millimeters": 0.001,
        "cm": 0.01, "centimeter": 0.01, "centimeters": 0.01,
        "km": 1000.0, "kilometer": 1000.0, "kilometers": 1000.0,
        "in": 0.0254, "inch": 0.0254, "inches": 0.0254,
        "ft": 0.3048, "foot": 0.3048, "feet": 0.3048,
        "yd": 0.9144, "yard": 0.9144, "yards": 0.9144,
        "mi": 1609.344, "mile": 1609.344, "miles": 1609.344,
    },
    "mass": {  # base: kilogram
        "kg": 1.0, "kilogram": 1.0, "kilograms": 1.0,
        "g": 0.001, "gram": 0.001, "grams": 0.001,
        "mg": 1e-6, "milligram": 1e-6, "milligrams": 1e-6,
        "lb": 0.45359237, "pound": 0.45359237, "pounds": 0.45359237,
        "oz": 0.028349523125, "ounce": 0.028349523125, "ounces": 0.028349523125,
    },
    "time": {  # base: second
        "s": 1.0, "sec": 1.0, "second": 1.0, "seconds": 1.0,
        "min": 60.0, "minute": 60.0, "minutes": 60.0,
        "h": 3600.0, "hr": 3600.0, "hour": 3600.0, "hours": 3600.0,
        "day": 86400.0, "days": 86400.0,
    },
    "area": {  # base: square meter
        "m2": 1.0, "m^2": 1.0, "sqm": 1.0,
        "cm2": 0.0001, "cm^2": 0.0001,
        "km2": 1e6, "km^2": 1e6,
        "ha": 10000.0, "hectare": 10000.0,
        "acre": 4046.8564224,
    },
    "volume": {  # base: cubic meter
        "m3": 1.0, "m^3": 1.0,
        "l": 0.001, "liter": 0.001, "litre": 0.001,
        "ml": 1e-6,
        "cm3": 1e-6, "cm^3": 1e-6, "cc": 1e-6,
        "gal": 0.003785411784, "gallon": 0.003785411784,
    },
    "speed": {  # base: meter / second
        "m/s": 1.0, "mps": 1.0,
        "km/h": 1000.0 / 3600.0, "kph": 1000.0 / 3600.0,
        "mph": 1609.344 / 3600.0,
        "knot": 1852.0 / 3600.0,
    },
    "pressure": {  # base: pascal
        "pa": 1.0, "pascal": 1.0,
        "kpa": 1000.0, "bar": 100000.0, "atm": 101325.0,
        "psi": 6894.757293168,
    },
    "energy": {  # base: joule
        "j": 1.0, "joule": 1.0,
        "kj": 1000.0,
        "cal": 4.184, "kcal": 4184.0,
        "wh": 3600.0, "kwh": 3.6e6,
        "ev": 1.602176634e-19,
    },
    "power": {  # base: watt
        "w": 1.0, "watt": 1.0,
        "kw": 1000.0,
        "hp": 745.699872,  # mechanical horsepower
    },
    "data": {  # base: byte
        "b": 1.0, "byte": 1.0,
        "kb": 1024.0, "kib": 1024.0,
        "mb": 1024.0**2, "gb": 1024.0**3, "tb": 1024.0**4,
        "bit": 1.0 / 8.0,
    },
    "angle": {  # base: radian
        "rad": 1.0, "radian": 1.0, "radians": 1.0,
        "deg": math.pi / 180.0, "degree": math.pi / 180.0,
    },
    "force": {  # base: newton
        "n": 1.0, "newton": 1.0,
        "kn": 1000.0, "kN": 1000.0,
        "lbf": 4.4482216152605, "pound-force": 4.4482216152605,
    },
    "frequency": {  # base: hertz
        "hz": 1.0, "hertz": 1.0,
        "khz": 1e3, "mhz": 1e6, "ghz": 1e9,
        "rpm": 1.0 / 60.0,
    },
    "electric_current": {  # base: ampere
        "a": 1.0, "amp": 1.0, "ampere": 1.0,
        "ma": 1e-3,
    },
    "voltage": {  # base: volt
        "v": 1.0, "volt": 1.0,
        "mv": 1e-3, "kv": 1e3,
    },
    "resistance": {  # base: ohm
        "ohm": 1.0, "ω": 1.0, "ohms": 1.0,
        "kohm": 1e3, "kω": 1e3, "mohm": 1e-3,
    },
    "capacitance": {  # base: farad
        "f": 1.0, "farad": 1.0,
        "mf": 1e-3, "uf": 1e-6, "nf": 1e-9, "pf": 1e-12,
    },
    "inductance": {  # base: henry
        "h": 1.0, "henry": 1.0,
        "mh": 1e-3, "uh": 1e-6,
    },
    "luminous_flux": {  # base: lumen
        "lm": 1.0, "lumen": 1.0,
    },
    "luminous_intensity": {  # base: candela
        "cd": 1.0, "candela": 1.0,
    },
    "illuminance": {  # base: lux
        "lx": 1.0, "lux": 1.0,
    },
    "amount": {  # base: mole
        "mol": 1.0, "mole": 1.0,
        "mmol": 1e-3, "umol": 1e-6, "μmol": 1e-6,
    },
    "concentration": {  # base: mol per liter (M)
        "m": 1.0, "molar": 1.0, "mol/l": 1.0, "mol/liter": 1.0,
        "mmol/l": 1e-3, "mol/m3": 1000.0,
    },
    "magnetic_flux_density": {  # base: tesla
        "t": 1.0, "tesla": 1.0,
        "gauss": 1e-4,
    },
    "frequency_time": {
    },
}

def _temp_to_kelvin(value: float, unit: str) -> float:
    u = unit.strip().lower()
    if u in ("c", "celsius", "°c"):
        return value + 273.15
    if u in ("f", "fahrenheit", "°f"):
        return (value - 32.0) * 5.0 / 9.0 + 273.15
    if u in ("k", "kelvin", "kelvins", "°k"):
        return value
    raise ValueError(f"Unsupported temperature unit: {unit}")

def _kelvin_to_temp(value_k: float, unit: str) -> float:
    u = unit.strip().lower()
    if u in ("c", "celsius", "°c"):
        return value_k - 273.15
    if u in ("f", "fahrenheit", "°f"):
        return (value_k - 273.15) * 9.0 / 5.0 + 32.0
    if u in ("k", "kelvin", "kelvins", "°k"):
        return value_k
    raise ValueError(f"Unsupported temperature unit: {unit}")

def list_quantities() -> List[str]:
    return sorted(list(_UNIT_MAPS.keys()) + ["temperature"])

def list_units(quantity: str) -> List[str]:
    q = quantity.strip().lower()
    if q == "temperature":
        return ["C", "F", "K"]
    if q in _UNIT_MAPS:
        return sorted(set(_UNIT_MAPS[q].keys()))
    raise ValueError(f"Unknown quantity: {quantity}")

def convert(quantity: str, value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert value from from_unit to to_unit for given quantity.
    """
    q = quantity.strip().lower()
    if q == "temperature":
        k = _temp_to_kelvin(value, from_unit)
        return _kelvin_to_temp(k, to_unit)

    if q not in _UNIT_MAPS:
        raise ValueError(f"Unsupported quantity: {quantity}")

    units = _UNIT_MAPS[q]
    units_l = {k.strip().lower(): v for k, v in units.items()}
    fu = from_unit.strip().lower()
    tu = to_unit.strip().lower()

    if fu not in units_l:
        raise ValueError(f"Unknown unit for {quantity}: {from_unit}")
    if tu not in units_l:
        raise ValueError(f"Unknown unit for {quantity}: {to_unit}")

    base_value = value * units_l[fu]   # convert to base unit
    result = base_value / units_l[tu]
    return result

def _cli():
    print("UnitConverter CLI. Supported quantities:")
    for q in list_quantities():
        print(" -", q)
    try:
        while True:
            q = input("\nQuantity (or 'quit'): ").strip()
            if not q or q.lower() in ("quit", "q", "exit"):
                break
            try:
                print("Available units:", ", ".join(list_units(q)))
            except Exception as e:
                print("Error:", e)
                continue
            try:
                v = float(input("Value: ").strip())
                fu = input("From unit: ").strip()
                tu = input("To unit: ").strip()
                out = convert(q, v, fu, tu)
                print(f"{v} {fu} = {out} {tu}")
            except Exception as e:
                print("Conversion error:", e)
    except (KeyboardInterrupt, EOFError):
        print("\nExiting.")
        return

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if len(sys.argv) >= 5:
            try:
                _, qty, val, fu, tu = sys.argv[:5]
                valf = float(val)
                res = convert(qty, valf, fu, tu)
                print(res)
            except Exception as e:
                print("Error:", e)
                print("Usage: unitconverter.py [quantity value from_unit to_unit]")
        else:
            print("Usage: unitconverter.py [quantity value from_unit to_unit]")
            print("Example: python unitconverter.py length 10 m ft")
    else:
        _cli()
