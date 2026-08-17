# app/models.py
from sqlalchemy import Column, Integer, Numeric, String, DateTime, func
from database import Base


class Advertisement(Base):
    __tablename__ = "advertisements"

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    description = Column(String)
    price = Column(Numeric)
    create_date = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "create_date": self.create_date.isoformat() if self.create_date else None,
        }
