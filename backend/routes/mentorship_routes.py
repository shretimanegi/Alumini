# mentorship_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers import request_mentorship, list_mentorships_for_alumni
mentorship_bp = Blueprint("mentorships", __name__)

@mentorship_bp.route("/request", methods=["POST"])
@jwt_required()
def request_route():
    identity = get_jwt_identity()
    if identity.get("type") != "alumni":
        return jsonify({"message":"Only alumni can offer mentorships"}), 403
    data = request.json or {}
    res = request_mentorship(identity.get("id"), data)
    return jsonify(res), (201 if res.get("success") else 400)

@mentorship_bp.route("/me", methods=["GET"])
@jwt_required()
def my_mentorships():
    identity = get_jwt_identity()
    if identity.get("type") != "alumni":
        return jsonify({"message":"Only alumni"}), 403
    res = list_mentorships_for_alumni(identity.get("id"))
    return jsonify(res)
