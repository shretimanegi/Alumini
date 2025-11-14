# event_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers import create_event, list_events
event_bp = Blueprint("events", __name__)

@event_bp.route("/", methods=["GET"])
def events_list():
    return jsonify(list_events())

@event_bp.route("/", methods=["POST"])
@jwt_required()
def create_event_route():
    identity = get_jwt_identity()
    if identity.get("type") != "alumni":
        return jsonify({"message":"Only alumni can create events"}), 403
    data = request.json or {}
    res = create_event(data, identity.get("id"))
    if res.get("success"):
        return jsonify(res), 201
    return jsonify(res), 400
