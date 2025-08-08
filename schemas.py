
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal, Dict, Any

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Literal["customer", "merchant", "courier"] = "customer"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class PilotSignupIn(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    role: Optional[str] = None
    source: Optional[str] = None

class QuoteIn(BaseModel):
    # Prefer distance_km (from secure frontend function). You can also pass lat/lng.
    origin: Optional[str] = None
    destination: Optional[str] = None
    distance_km: Optional[float] = None

    origin_lat: Optional[float] = None
    origin_lng: Optional[float] = None
    dest_lat: Optional[float] = None
    dest_lng: Optional[float] = None

    weight_kg: float = 1.0
    size_factor: float = 1.0  # capped by service
    item_type: str = "general"
    urgency: Literal["standard", "rush", "express"] = "standard"
    vehicle: Literal["walk", "bike", "car", "suv", "van", "truck"] = "car"
    weather_code: Optional[int] = None  # Optional OpenWeather code

class PriceBreakdown(BaseModel):
    currency: str = "USD"
    base_fare: float
    distance_cost: float
    weight_fee: float
    multipliers: Dict[str, float]
    weather_surcharge: float
    total: float

class QuoteOut(BaseModel):
    price_total: float
    breakdown: PriceBreakdown
    inputs: Dict[str, Any]
