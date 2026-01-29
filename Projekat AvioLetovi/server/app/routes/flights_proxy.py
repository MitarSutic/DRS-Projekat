import requests
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

flights_bp = Blueprint("flights_proxy", __name__)

FLIGHT_SERVICE_URL = "http://localhost:5001/api/flights"

@flights_bp.route("/flights", methods=["GET"])
@jwt_required()
def get_flights():
    response = requests.get(FLIGHT_SERVICE_URL)
    return jsonify(response.json()), response.status_code

@flights_bp.route("/flights", methods=["POST"])
@jwt_required()
def create_flight():
    data = request.json
    response = requests.post(FLIGHT_SERVICE_URL, json=data)
    return jsonify(response.json()), response.status_code