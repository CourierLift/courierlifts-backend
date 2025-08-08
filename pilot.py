
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import PilotSignup
from ..schemas import PilotSignupIn

router = APIRouter()

@router.post("/signup")
def pilot_signup(data: PilotSignupIn, db: Session = Depends(get_db)):
    rec = PilotSignup(email=data.email, name=data.name, role=data.role, source=data.source)
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return {"ok": True, "id": rec.id}
