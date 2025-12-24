from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models.user import User
from app.extensions import db

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
        datum_rodjenja=data.get("datumrodjenja"),
        pol=data.get("pol"),
        drzava=data.get("drzava"),
        ulica=data.get("ulica"),
        broj=data.get("broj"),
        stanje_racuna=data.get("stanjeracuna", 0.0),
    )
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return jsonify(msg="User registered"), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data["email"]).first()

    if not user or not user.check_password(data["password"]):
        return jsonify(msg="Bad credentials"), 401

    token = create_access_token(identity={
        "id": user.id,
        "role": user.uloga
    })

    return jsonify(access_token=token), 200