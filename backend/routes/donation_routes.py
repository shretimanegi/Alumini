# donation_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers import create_donation, donation_history
donation_bp = Blueprint("donations", __name__)

@donation_bp.route("/", methods=["POST"])
@jwt_required()
def donate():
    identity = get_jwt_identity()
    if identity.get("type") != "alumni":
        return jsonify({"message":"Only alumni can donate"}), 403
    data = request.json or {}
    res = create_donation(identity.get("id"), data)
    return jsonify(res), (201 if res.get("success") else 400)

@donation_bp.route("/me", methods=["GET"])
@jwt_required()
def my_donations():
    identity = get_jwt_identity()
    if identity.get("type") != "alumni":
        return jsonify({"message":"Only alumni"}), 403
    hist = donation_history(identity.get("id"))
    return jsonify(hist)
