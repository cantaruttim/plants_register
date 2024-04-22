from sqlalchemy import Column, Integer, String
from database import Base


class Plant(Base):
    __tablename__ = 'plants'

    id = Column(Integer, primary_key=True)
    plant_name = Column(String(150))
    plant_scientific_name = Column(String(150))
    plant_type = Column(String(150))
    ideal_temperature = Column(Integer)
    ideal_umidity = Column(Integer)

    def __repr__(self):
        return '<Plant %r>' % (self.id)