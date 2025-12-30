from app.extensions import db, bcrypt
from datetime import datetime, timedelta

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
    kreiran_at = db.Column(db.DateTime, default=datetime.now,name="KreiranAt")

    pokusaji = db.Column(db.Integer, name="Pokusaji", default=0, nullable=False)
    blokiranDo = db.Column( db.DateTime, name="BlokiranDo", nullable=True)


    def set_password(self, password):
        self.lozinka_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.lozinka_hash, password)
    
    def is_locked(self) ->bool:
        return self.blokiranDo and datetime.now() < self.blokiranDo
    
    def register_failed_attempts(self):
        self.pokusaji +=1
        if self.pokusaji >=3:
            self.blokiranDo = datetime.now() + timedelta(seconds = 10)
            self.pokusaji = 0

    def reset_attempts(self):
        self.pokusaji = 0
        self.blokiranDo = None
