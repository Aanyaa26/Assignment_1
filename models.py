from sqlalchemy import Column, Integer, String
from database import Base

class AddressDB(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, index=True)
    hn = Column(Integer, nullable=False)
    ap = Column(String(255), nullable=False)
    pincode = Column(Integer, nullable=False)
