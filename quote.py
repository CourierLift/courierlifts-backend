
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Quote
from ..schemas import QuoteIn, QuoteOut, PriceBreakdown
from ..services.geo import haversine_km
from ..services.pricing import compute_price

router = APIRouter()

@router.post("/estimate", response_model=QuoteOut)
def estimate_quote(payload: QuoteIn, db: Session = Depends(get_db)):
    # Determine distance
    distance_km = None
    if payload.distance_km is not None:
        distance_km = max(0.0, payload.distance_km)
    elif all(v is not None for v in [payload.origin_lat, payload.origin_lng, payload.dest_lat, payload.dest_lng]):
        distance_km = haversine_km(payload.origin_lat, payload.origin_lng, payload.dest_lat, payload.dest_lng)
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Provide distance_km or lat/lng coordinates")

    breakdown_dict = compute_price(
        distance_km=distance_km,
        weight_kg=payload.weight_kg,
        size_factor=payload.size_factor,
        item_type=payload.item_type,
        urgency=payload.urgency,
        vehicle=payload.vehicle,
        weather_code=payload.weather_code,
    )

    quote = Quote(
        origin=payload.origin,
        destination=payload.destination,
        distance_km=distance_km,
        price_total=breakdown_dict["total"],
        breakdown=str(breakdown_dict),
    )
    db.add(quote)
    db.commit()
    db.refresh(quote)

    breakdown = PriceBreakdown(**breakdown_dict)

    return QuoteOut(
        price_total=breakdown.total,
        breakdown=breakdown,
        inputs=payload.model_dump(),
    )
