from fastapi import FastAPI, Depends # import - depends helps to inject database connection
from sqlalchemy.orm import Session   # session represents the db connection
from database import SessionLocal, engine, Base  # engine creates connection to MySQL , session local creates DB session , Base creates base class for DB tables (all imported from database.py)
from models import AddressDB # imports SQLAlchemy model 
from pydantic import BaseModel, Field # for validation

app = FastAPI()  # creating the fast api application

Base.metadata.create_all(bind=engine) # if table isn't there, create one

class Address(BaseModel): # defines the structure of the icoming payload
    hn: int
    ap: str
    pincode: int = Field(..., ge=100000, le=999999)

class Payload(BaseModel):  # this ensures that the payload must look like this
    address: Address

def get_db():  
    db = SessionLocal()   #It creates db connection and close it safely
    try:
        yield db  #gives DB connection to FastApi
    finally:
        db.close() # closes after use

@app.post("/address")  #endpoint
def create_address(payload: Payload, db: Session = Depends(get_db)):
    addr = payload.address #extracting as an object (deserialization)

    db_address = AddressDB(
        hn=addr.hn,
        ap=addr.ap,
        pincode=addr.pincode
    )

    db.add(db_address) #saving data into the table
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
