#!/usr/bin/python3

from app.extensions import db
from app.models.BaseModel import BaseModel

class Place(BaseModel):
    __tablename__ = 'places'  # ✅ Define table name

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False, default=0.0)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)  # ✅ Foreign key reference

    owner = db.relationship('User', backref='places', lazy=True)  # ✅ Define relationship

    def __repr__(self):
        return f"<Place {self.title}>"

