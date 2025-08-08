
# Courier Lifts Backend (FastAPI Minimal MVP)

A clean, battery-included FastAPI service for the Courier Lifts MVP.

## What's inside

- FastAPI app with CORS for your Netlify domain
- JWT auth: register/login
- SQLite via SQLAlchemy
- Pilot signup endpoint
- Quote estimate endpoint with pricing engine (distance/weight/size/item/urgency/vehicle + optional weather surcharge)
- Haversine distance helper (if you pass lat/lng) and support for client-provided distance_km
- Optional OpenWeather hook (uses env key if provided, otherwise skipped)

## Endpoints (summary)

- `POST /auth/register` — create user
- `POST /auth/login` — get JWT
- `POST /pilot/signup` — capture pilot interest
- `POST /quote/estimate` — return price breakdown

> Tip: For addresses, your frontend should call Google Distance Matrix via a Netlify Function and pass `distance_km` to this backend. If you already have lat/lng, you can send those and we'll compute Haversine.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt

# Copy and edit env
cp .env.example .env

# Run
uvicorn app.main:app --reload
```

## .env

```
SECRET_KEY=change_me
ACCESS_TOKEN_EXPIRE_MINUTES=120
DATABASE_URL=sqlite:///./courierlifts.db

# Optional (weather)
OPENWEATHER_API_KEY=
```

## Deployment ideas

- Render / Railway / Fly.io
- Or Dockerize later; this repo is intentionally simple for speed.
