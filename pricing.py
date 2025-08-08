
from typing import Dict

ITEM_MULTIPLIER = {
    "general": 1.0,
    "documents": 0.95,
    "groceries": 1.05,
    "electronics": 1.2,
    "furniture": 1.35,
    "appliances": 1.4,
}

URGENCY_MULTIPLIER = {
    "standard": 1.0,
    "rush": 1.25,
    "express": 1.5,
}

VEHICLE_MULTIPLIER = {
    "walk": 0.9,
    "bike": 1.0,
    "car": 1.05,
    "suv": 1.1,
    "van": 1.2,
    "truck": 1.35,
}

def clamp_size_factor(x: float, lo: float = 0.8, hi: float = 1.8) -> float:
    return max(lo, min(hi, x))

def compute_price(distance_km: float, weight_kg: float, size_factor: float, item_type: str, urgency: str, vehicle: str, weather_code: int | None) -> Dict:
    base_fare = 4.0
    per_km = 1.25
    weight_fee = 0.10 * max(0.0, weight_kg)  # $0.10 per kg

    size = clamp_size_factor(size_factor)
    item_mult = ITEM_MULTIPLIER.get(item_type, 1.0)
    urg_mult = URGENCY_MULTIPLIER.get(urgency, 1.0)
    veh_mult = VEHICLE_MULTIPLIER.get(vehicle, 1.05)

    distance_cost = per_km * max(0.0, distance_km)

    # Weather surcharge (simple): rain/snow/thunder bump
    weather_surcharge = 0.0
    if weather_code is not None:
        if 200 <= weather_code < 600:  # thunderstorm/drizzle/rain
            weather_surcharge = 1.25
        elif 600 <= weather_code < 700:  # snow
            weather_surcharge = 1.75
        elif 700 <= weather_code < 800:  # fog/mist
            weather_surcharge = 0.75

    subtotal = base_fare + distance_cost + weight_fee + weather_surcharge
    multiplier = size * item_mult * urg_mult * veh_mult
    total = round(subtotal * multiplier, 2)

    return {
        "currency": "USD",
        "base_fare": round(base_fare, 2),
        "distance_cost": round(distance_cost, 2),
        "weight_fee": round(weight_fee, 2),
        "multipliers": {
            "size": round(size, 2),
            "item": item_mult,
            "urgency": urg_mult,
            "vehicle": veh_mult,
        },
        "weather_surcharge": round(weather_surcharge, 2),
        "total": total,
    }
