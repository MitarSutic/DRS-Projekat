from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models.user import User
from app.extensions import db

admin_bp = Blueprint("admin", __name__)

# Helper: proverava da li je korisnik admin
def is_admin():
    claims = get_jwt()  # ovo vraća dict sa svim claim-ovima iz JWT
    return claims.get("role") == "ADMINISTRATOR"

#Lista svih korisnika
@admin_bp.route("/users", methods=["GET"])
@jwt_required()
def list_users():
    if not is_admin():
        return jsonify(msg="Nemate ovlašćenje"), 403

    users = User.query.all()
    users_list = [
        {
            "id": u.id,
            "ime": u.ime,
            "prezime": u.prezime,
            "email": u.email,
            "uloga": u.uloga
        } for u in users
    ]
    return jsonify(users_list), 200

# Promena uloge
@admin_bp.route("/users/<int:user_id>/role", methods=["PATCH"])
@jwt_required()
def change_role(user_id):
    if not is_admin():
        return jsonify(msg="Nemate ovlašćenje"), 403

    data = request.json
    new_role = data.get("uloga")
    if new_role not in ["KORISNIK", "MENADZER", "ADMINISTRATOR"]:
        return jsonify(msg="Nevalidna uloga"), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify(msg="Korisnik ne postoji"), 404

    user.uloga = new_role
    db.session.commit()
    return jsonify(msg=f"Uloga korisnika {user.ime} {user.prezime} promenjena u {new_role}"), 200

# Brisanje korisnika
@admin_bp.route("/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    if not is_admin():
        return jsonify(msg="Nemate ovlašćenje"), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify(msg="Korisnik ne postoji"), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify(msg=f"Korisnik {user.email} obrisan"), 200
