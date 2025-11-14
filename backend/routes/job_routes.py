# job_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers import post_job, list_jobs
job_bp = Blueprint("jobs", __name__)

@job_bp.route("/", methods=["GET"])
def get_jobs():
    return jsonify(list_jobs())

@job_bp.route("/", methods=["POST"])
@jwt_required()
def create_job():
    identity = get_jwt_identity()
    if identity.get("type") != "alumni":
        return jsonify({"message":"Only alumni can post jobs"}), 403
    data = request.json or {}
    res = post_job(identity.get("id"), data)
    return jsonify(res), (201 if res.get("success") else 400)
