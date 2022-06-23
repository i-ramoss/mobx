from extensions import db
from .immobile_model import Immobile


class Apartment(Immobile):
    __tablename__ = "apartments"

    id = db.Column(db.String, db.ForeignKey("immobiles.id"), primary_key=True)
    floor = db.Column(db.Integer)

    __mapper_args__ = {"polymorphic_identity": "apartments"}

    def __init__(self, description, daily_rate, fine_amount, area, is_available, floor):
        super().__init__(description, daily_rate, fine_amount, area, is_available)
        self.floor = floor

    def transform_to_json(self):
        return {
            "id": self.id,
            "description": self.description,
            "daily_rate": self.daily_rate,
            "fine_amount": self.fine_amount,
            "area": self.area,
            "is_available": self.is_available,
            "floor": self.floor,
            "type": self.type,
            "address": self.address.transform_to_json(),
        }
