from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models.user import User
from app.extensions import db

from app.login_attempt_service import(
    is_blocked,
    register_failed_attempt,
    reset_attempts
)
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    if User.query.filter_by(email=data["email"]).first():
        return jsonify(msg="Email already exists"), 400

    user = User(
        ime=data.get("ime"),
        prezime=data.get("prezime"),
        email=data["email"],
        datum_rodjenja=data.get("datumRodjenja"),
        pol=data.get("pol", ""),
        drzava=data.get("drzava",""),
        ulica=data.get("ulica",""),
        broj=data.get("broj",""),
        stanje_racuna=data.get("stanjeracuna", 0.0),
    )
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return jsonify(msg="User registered"), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json or {}
    # email = data.get("email")
    password = data.get("password")

    # if not email or not password:
    #     return jsonify(msg="Email i lozinkasdg su obavezni"), 400
    
    user = User.query.filter_by(email=data["email"]).first()

    if not user:
        return jsonify(msg="Korisnik ne postoji!"), 401

    if user.is_locked():
        return jsonify(msg="Nalog je privremeno blokiran. Pokusajte kasnije."), 403
    
    if not user.check_password(password):
        user.register_failed_attempts()
        db.session.commit()
        return jsonify(msg="Pogrešna lozinka"), 401

    
    user.reset_attempts()
    db.session.commit()

    token = create_access_token(
    identity=str(user.id),
    additional_claims={"role": user.uloga}
    )
    return jsonify(access_token=token), 200