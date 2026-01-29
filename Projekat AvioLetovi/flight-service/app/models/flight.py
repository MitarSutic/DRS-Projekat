from app.extensions import db
from datetime import datetime

class Flight(db.Model):
    __tablename__ = "Flights"

    id = db.Column(db.Integer, primary_key=True, name="Id")
    Naziv = db.Column(db.String(100), nullable=False, name="Naziv")
    AirlineId = db.Column(db.Integer, nullable=True,name="AirlineId")
    DuzinaLeta= db.Column(db.Integer, nullable=True,name="DuzinaLeta")
    TrajanjeLeta = db.Column(db.Integer, nullable=True, name="TrajanjeLeta")
    VremePolaska = db.Column(db.DateTime,default=datetime.now, nullable=True, name="VremePolaska")
    AerodromPolaska = db.Column(db.String(100), nullable=True,name="AerodromPolaska")
    AerodromDolaska = db.Column(db.String(100), nullable=True,name="AerodromDOlaska")
    KreiraoUserId = db.Column(db.Integer, nullable=True,name="KreiraoUserId")
    CenaKarte = db.Column(db.Float, nullable=True,name="CenaKarte")
    Status = db.Column(db.String(20), nullable=True,name="Status", default = "PENDING")