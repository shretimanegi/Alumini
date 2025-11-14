# controllers.py
from models import SessionLocal, Alumni, Student, Event, Donation, Mentorship, Job, Department, Batch
from sqlalchemy.exc import IntegrityError
from utils import hash_password, check_password
from datetime import datetime

def create_alumni(payload):
    session = SessionLocal()
    try:
        new = Alumni(
            name=payload.get("name"),
            email=payload.get("email"),
            phone=payload.get("phone"),
            batch_id=payload.get("batch_id"),
            department_id=payload.get("department_id"),
            current_position=payload.get("current_position"),
            password=hash_password(payload.get("password"))
        )
        session.add(new)
        session.commit()
        return {"success": True, "alumni_id": new.alumni_id}
    except IntegrityError as e:
        session.rollback()
        return {"success": False, "message": "Email already exists"}
    finally:
        session.close()

def login_alumni(email, password):
    session = SessionLocal()
    try:
        user = session.query(Alumni).filter(Alumni.email == email).first()
        if user and check_password(password, user.password):
            return {"success": True, "alumni_id": user.alumni_id, "name": user.name, "email": user.email}
        return {"success": False, "message": "Invalid credentials"}
    finally:
        session.close()

def create_student(payload):
    session = SessionLocal()
    try:
        new = Student(
            name=payload.get("name"),
            email=payload.get("email"),
            phone=payload.get("phone"),
            batch_id=payload.get("batch_id"),
            department_id=payload.get("department_id"),
            password=hash_password(payload.get("password"))
        )
        session.add(new)
        session.commit()
        return {"success": True, "student_id": new.student_id}
    except IntegrityError:
        session.rollback()
        return {"success": False, "message": "Email already exists"}
    finally:
        session.close()

def login_student(email, password):
    session = SessionLocal()
    try:
        user = session.query(Student).filter(Student.email == email).first()
        if user and check_password(password, user.password):
            return {"success": True, "student_id": user.student_id, "name": user.name, "email": user.email}
        return {"success": False, "message": "Invalid credentials"}
    finally:
        session.close()

def create_event(payload, alumni_id):
    session = SessionLocal()
    try:
        e = Event(
            event_title=payload.get("event_title"),
            event_date=datetime.strptime(payload.get("event_date"), "%Y-%m-%d").date(),
            event_description=payload.get("event_description"),
            created_by=alumni_id
        )
        session.add(e)
        session.commit()
        return {"success": True, "event_id": e.event_id}
    except Exception as ex:
        session.rollback()
        return {"success": False, "message": str(ex)}
    finally:
        session.close()

def list_events():
    session = SessionLocal()
    try:
        events = session.query(Event).all()
        return [{"event_id": e.event_id, "event_title": e.event_title, "event_date": str(e.event_date), "event_description": e.event_description, "created_by": e.created_by} for e in events]
    finally:
        session.close()

def create_donation(alumni_id, payload):
    session = SessionLocal()
    try:
        d = Donation(
            alumni_id=alumni_id,
            amount=payload.get("amount"),
            purpose=payload.get("purpose")
        )
        session.add(d)
        session.commit()
        return {"success": True, "donation_id": d.donation_id}
    except Exception as e:
        session.rollback()
        return {"success": False, "message": str(e)}
    finally:
        session.close()

def donation_history(alumni_id):
    session = SessionLocal()
    try:
        rows = session.query(Donation).filter(Donation.alumni_id == alumni_id).all()
        return [{"donation_id": r.donation_id, "amount": r.amount, "purpose": r.purpose, "date": str(r.date)} for r in rows]
    finally:
        session.close()

def request_mentorship(alumni_id, payload):
    session = SessionLocal()
    try:
        m = Mentorship(
            alumni_id=alumni_id,
            student_id=payload.get("student_id"),
            status="pending"
        )
        session.add(m)
        session.commit()
        return {"success": True, "mentor_id": m.mentor_id}
    finally:
        session.close()

def list_mentorships_for_alumni(alumni_id):
    session = SessionLocal()
    try:
        rows = session.query(Mentorship).filter(Mentorship.alumni_id == alumni_id).all()
        return [{"mentor_id": r.mentor_id, "student_id": r.student_id, "status": r.status} for r in rows]
    finally:
        session.close()

def post_job(alumni_id, payload):
    session = SessionLocal()
    try:
        j = Job(
            title=payload.get("title"),
            description=payload.get("description"),
            posted_by=alumni_id,
            deadline=datetime.strptime(payload.get("deadline"), "%Y-%m-%d").date() if payload.get("deadline") else None
        )
        session.add(j)
        session.commit()
        return {"success": True, "job_id": j.job_id}
    finally:
        session.close()

def list_jobs():
    session = SessionLocal()
    try:
        rows = session.query(Job).all()
        return [{"job_id": r.job_id, "title": r.title, "description": r.description, "deadline": str(r.deadline) if r.deadline else None, "posted_by": r.posted_by} for r in rows]
    finally:
        session.close()

def get_alumni_profile(alumni_id):
    session = SessionLocal()
    try:
        a = session.get(Alumni, alumni_id)
        if not a:
            return None
        return {"alumni_id": a.alumni_id, "name": a.name, "email": a.email, "phone": a.phone, "batch_id": a.batch_id, "department_id": a.department_id, "current_position": a.current_position}
    finally:
        session.close()

def get_student_profile(student_id):
    session = SessionLocal()
    try:
        s = session.get(Student, student_id)
        if not s:
            return None
        return {"student_id": s.student_id, "name": s.name, "email": s.email, "phone": s.phone, "batch_id": s.batch_id, "department_id": s.department_id}
    finally:
        session.close()
