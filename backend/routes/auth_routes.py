# auth_routes.py
from flask import Blueprint, request, jsonify
from controllers import create_alumni, login_alumni, create_student, login_student
from flask_jwt_extended import create_access_token
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/alumni/register", methods=["POST"])
def alumni_register():
    data = request.json or {}
    res = create_alumni(data)
    if res.get("success"):
        return jsonify({"message":"registered","alumni_id":res.get("alumni_id")}), 201
    return jsonify({"message": res.get("message","error")}), 400

@auth_bp.route("/alumni/login", methods=["POST"])
def alumni_login():
    data = request.json or {}
    res = login_alumni(data.get("email"), data.get("password"))
    if res.get("success"):
        token = create_access_token(identity={"type":"alumni","id":res.get("alumni_id")})
        return jsonify({"token":token, "user": {"id":res.get("alumni_id"), "name":res.get("name"), "email":res.get("email")}})
    return jsonify({"message":"invalid credentials"}), 401

@auth_bp.route("/student/register", methods=["POST"])
def student_register():
    data = request.json or {}
    res = create_student(data)
    if res.get("success"):
        return jsonify({"message":"registered","student_id":res.get("student_id")}), 201
    return jsonify({"message": res.get("message","error")}), 400

@auth_bp.route("/student/login", methods=["POST"])
def student_login():
    data = request.json or {}
    res = login_student(data.get("email"), data.get("password"))
    if res.get("success"):
        token = create_access_token(identity={"type":"student","id":res.get("student_id")})
        return jsonify({"token":token, "user": {"id":res.get("student_id"), "name":res.get("name"), "email":res.get("email")}})
    return jsonify({"message":"invalid credentials"}), 401
