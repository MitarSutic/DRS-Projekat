from flask import Blueprint, request, jsonify
from app.models.flight import Flight
from app.extensions import db
from flask_socketio import SocketIO
from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt

flights_bp = Blueprint("flights_bp", __name__)

# Ovo je samo referenca, SocketIO ćemo injektovati kasnije
socketio = None

def init_socketio(sio: SocketIO):
    global socketio
    socketio = sio

# ======== Role dekorator ========
from flask_jwt_extended import get_jwt_identity

def role_required(role):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if claims.get("role") != role:
                return {"msg": "Forbidden"}, 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator



# ======== GET svi letovi ========
@flights_bp.route("/", methods=["GET"])
def get_flights():
    flights = Flight.query.all()
    result = []
    for f in flights:
        result.append({
            "id": f.id,
            "naziv": f.Naziv,
            "status": f.Status,
            "airlineId": f.AirlineId,
            "aerodromPolaska": f.AerodromPolaska,
            "aerodromDolaska": f.AerodromDolaska,
            "cenaKarte": f.CenaKarte
        })
    return jsonify(result)

# ======== Kreiranje leta (samo manager) ========
@flights_bp.route("/", methods=["POST"])
@role_required("MENADZER")
def create_flight():
    data = request.json
    flight = Flight(
        Naziv=data["naziv"],
        AirlineId=data["airlineId"],
        DuzinaLeta=data["duzinaLeta"],
        TrajanjeLeta=data["trajanjeLeta"],
        AerodromPolaska=data["aerodromPolaska"],
        AerodromDolaska=data["aerodromDolaska"],
        KreiraoUserId=data["kreiraoUserId"],
        CenaKarte=data["cenaKarte"],
        Status="pending"
    )
    db.session.add(flight)
    db.session.commit()

    if socketio:
        socketio.emit("new_flight_pending", {
            "id": flight.id,
            "naziv": flight.Naziv,
            "status": flight.Status
        }, namespace="/admin")

    return jsonify({"message": "Flight created", "flightId": flight.id})

# ======== Odobravanje leta (samo admin) ========
@flights_bp.route("/<int:flight_id>/approve", methods=["POST"])
@role_required("ADMINISTRATOR")
def approve_flight(flight_id):
    flight = Flight.query.get(flight_id)
    if not flight:
        return jsonify({"message": "Flight not found"}), 404

    flight.Status = "approved"
    db.session.commit()

    if socketio:
        socketio.emit("flight_approved", {
            "id": flight.id,
            "naziv": flight.Naziv,
            "status": flight.Status
        }, namespace="/users")

    return jsonify({"message": "Flight approved"})

# ======== Odbijanje leta (samo admin) ========
@flights_bp.route("/<int:flight_id>/reject", methods=["POST"])
@role_required("ADMINISTRATOR")
def reject_flight(flight_id):
    flight = Flight.query.get(flight_id)
    if not flight:
        return jsonify({"message": "Flight not found"}), 404

    data = request.json
    reason = data.get("reason", "")
    flight.Status = "rejected"
    db.session.commit()

    if socketio:
        socketio.emit("flight_rejected", {
            "id": flight.id,
            "naziv": flight.Naziv,
            "status": flight.Status,
            "reason": reason
        }, namespace="/manager")

    return jsonify({"message": "Flight rejected"})

# ======== Brisanje leta (samo admin) ========
@flights_bp.route("/<int:flight_id>/delete", methods=["DELETE"])
@role_required("ADMINISTRATOR")
def delete_flight(flight_id):
    flight = Flight.query.get(flight_id)
    if not flight:
        return jsonify({"message": "Flight not found"}), 404

    # Fizičko brisanje
    db.session.delete(flight)
    db.session.commit()

    # Alternativa: soft delete
    # flight.Status = "deleted"
    # db.session.commit()

    return jsonify({"message": "Flight obrisan"})
