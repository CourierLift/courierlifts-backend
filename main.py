
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import auth, quote, pilot
from .database import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Courier Lifts Backend", version="0.1.0")

# CORS — adjust to your Netlify domain in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(pilot.router, prefix="/pilot", tags=["pilot"])
app.include_router(quote.router, prefix="/quote", tags=["quote"])

@app.get("/health")
def health():
    return {"status": "ok"}
