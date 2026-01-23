from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import AddressDB
from pydantic import BaseModel, Field

app = FastAPI()

Base.metadata.create_all(bind=engine)

class Address(BaseModel):
    hn: int
    ap: str
    pincode: int = Field(..., ge=100000, le=999999)

class Payload(BaseModel):
    address: Address

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/address")
def create_address(payload: Payload, db: Session = Depends(get_db)):
    addr = payload.address

    db_address = AddressDB(
        hn=addr.hn,
        ap=addr.ap,
        pincode=addr.pincode
    )

    db.add(db_address)
    db.commit()
    db.refresh(db_address)

    return {
        "message": "Address saved successfully",
        "data": {
            "id": db_address.id,
            "hn": db_address.hn,
            "ap": db_address.ap,
            "pincode": db_address.pincode
        }
    }
