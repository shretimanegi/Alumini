# app.py
from flask import Flask, jsonify
from config import SQLALCHEMY_DATABASE_URI, JWT_SECRET_KEY
from models import engine, Base
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.event_routes import event_bp
from routes.donation_routes import donation_bp
from routes.mentorship_routes import mentorship_bp
from routes.job_routes import job_bp

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
CORS(app)
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(event_bp, url_prefix="/api/events")
app.register_blueprint(donation_bp, url_prefix="/api/donations")
app.register_blueprint(mentorship_bp, url_prefix="/api/mentorships")
app.register_blueprint(job_bp, url_prefix="/api/jobs")

@app.route("/")
def index():
    return jsonify({"message":"Alumni Management API running"})

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    app.run(debug=True, host="0.0.0.0", port=5000)
