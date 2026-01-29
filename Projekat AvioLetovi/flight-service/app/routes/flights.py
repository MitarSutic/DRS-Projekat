from flask import Blueprint, request, jsonify
from app.models.flight import Flight
from app.extensions import db
from flask_socketio import SocketIO, emit

flights_bp = Blueprint("flights_bp", __name__)

# Ovo je samo referenca, SocketIO ćemo injektovati kasnije
socketio = None

def init_socketio(sio):
    global socketio
    socketio = sio

# GET svi letovi
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

# Kreiranje leta (menadžer)
@flights_bp.route("/", methods=["POST"])
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
        Status="pending"  # odmah pending
    )
    db.session.add(flight)
    db.session.commit()

    # emitovati event ka adminu
    if socketio:
        socketio.emit("new_flight_pending", {
            "id": flight.id,
            "naziv": flight.Naziv,
            "status": flight.Status
        }, namespace="/admin")

    return jsonify({"message": "Flight created", "flightId": flight.id})

# Admin odobrava let
@flights_bp.route("/<int:flight_id>/approve", methods=["POST"])
def approve_flight(flight_id):
    flight = Flight.query.get(flight_id)
    if not flight:
        return jsonify({"message": "Flight not found"}), 404

    flight.Status = "approved"
    db.session.commit()

    # Emit ka korisnicima ili frontu ako želiš
    if socketio:
        socketio.emit("flight_approved", {
            "id": flight.id,
            "naziv": flight.Naziv,
            "status": flight.Status
        }, namespace="/users")

    return jsonify({"message": "Flight approved"})

# Admin odbija let
@flights_bp.route("/<int:flight_id>/reject", methods=["POST"])
def reject_flight(flight_id):
    flight = Flight.query.get(flight_id)
    if not flight:
        return jsonify({"message": "Flight not found"}), 404

    data = request.json
    reason = data.get("reason", "")
    flight.Status = "rejected"
    db.session.commit()

    # Emit ka menadžeru
    if socketio:
        socketio.emit("flight_rejected", {
            "id": flight.id,
            "naziv": flight.Naziv,
            "status": flight.Status,
            "reason": reason
        }, namespace="/manager")

    return jsonify({"message": "Flight rejected"})