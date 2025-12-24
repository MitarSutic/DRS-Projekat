from app.extensions import db, bcrypt
from datetime import datetime

class User(db.Model):
    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True, name="Id")
    ime = db.Column(db.String(50), nullable=False,name="Ime")
    prezime = db.Column(db.String(50), nullable=False,name="Prezime")
    email = db.Column(db.String(120), unique=True, nullable=False,name="Email")
    lozinka_hash = db.Column(db.String(128), nullable=False,name="LozinkaHash")
    datum_rodjenja = db.Column(db.Date, nullable=False,name="DatumRodjenja")
    pol = db.Column(db.String(10),name="Pol")
    drzava = db.Column(db.String(50),name="Drzava")
    ulica = db.Column(db.String(100),name="Ulica")
    broj = db.Column(db.String(10),name="Broj")
    stanje_racuna = db.Column(db.Float, default=0.0,name="StanjeRacuna")
    uloga = db.Column(db.String(20), default="KORISNIK",name="Uloga")
    kreiran_at = db.Column(db.DateTime, default=datetime.utcnow,name="KreiranAt")

    def set_password(self, password):
        self.lozinka_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.lozinka_hash, password)
