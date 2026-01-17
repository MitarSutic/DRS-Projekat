from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.extensions import db

users_bp = Blueprint("users", __name__)


# ==============================
# GET /users/me
# ==============================
@users_bp.route("/me", methods=["GET"])
@jwt_required()
def get_my_profile():
    user_id = int(get_jwt_identity())

    user = User.query.get(user_id)
    if not user:
        return jsonify(msg="Korisnik ne postoji"), 404

    return jsonify({
        "id": user.id,
        "email": user.email,
        "ime": user.ime,
        "prezime": user.prezime,
        "datum_rodjenja": user.datum_rodjenja,
        "pol": user.pol,
        "drzava": user.drzava,
        "ulica": user.ulica,
        "broj": user.broj,
        "uloga": user.uloga
    }), 200


# ======================================
# PATCH /users/me
# Izmena korisnika
# ======================================
@users_bp.route("/me", methods=["PATCH"])
@jwt_required()
def update_my_profile():
    identity = get_jwt_identity()
    user_id = int(get_jwt_identity())

    user = User.query.get(user_id)
    if not user:
        return jsonify(msg="Korisnik ne postoji"), 404

    data = request.json or {}

    # dozvoljena polja za izmenu
    allowed_fields = [
        "ime",
        "prezime",
        "datum_rodjenja",
        "pol",
        "drzava",
        "ulica",
        "broj"
    ]

    for field in allowed_fields:
        if field in data:
            setattr(user, field, data[field])

    db.session.commit()

    return jsonify({
        "msg": "Profil uspešno ažuriran",
        "user": {
            "id": user.id,
            "email": user.email,
            "ime": user.ime,
            "prezime": user.prezime,
            "datum_rodjenja": user.datum_rodjenja,
            "pol": user.pol,
            "drzava": user.drzava,
            "ulica": user.ulica,
            "broj": user.broj,
            "uloga": user.uloga
        }
    }), 200
