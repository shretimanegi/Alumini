# models.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Text, Date
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import SQLALCHEMY_DATABASE_URI
from datetime import datetime

Base = declarative_base()

class Department(Base):
    __tablename__ = "departments"
    department_id = Column(Integer, primary_key=True, autoincrement=True)
    department_name = Column(String(150), nullable=False)

    alumni = relationship("Alumni", back_populates="department")
    students = relationship("Student", back_populates="department")

class Batch(Base):
    __tablename__ = "batches"
    batch_id = Column(Integer, primary_key=True, autoincrement=True)
    batch_year = Column(Integer, nullable=False)

    alumni = relationship("Alumni", back_populates="batch")
    students = relationship("Student", back_populates="batch")

class Alumni(Base):
    __tablename__ = "alumni"
    alumni_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False, unique=True)
    phone = Column(String(50))
    batch_id = Column(Integer, ForeignKey("batches.batch_id"))
    department_id = Column(Integer, ForeignKey("departments.department_id"))
    current_position = Column(String(200))
    password = Column(String(200), nullable=False)

    batch = relationship("Batch", back_populates="alumni")
    department = relationship("Department", back_populates="alumni")
    events = relationship("Event", back_populates="creator")
    donations = relationship("Donation", back_populates="alumni")
    mentorships = relationship("Mentorship", back_populates="mentor")
    jobs = relationship("Job", back_populates="poster")

class Student(Base):
    __tablename__ = "students"
    student_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False, unique=True)
    phone = Column(String(50))
    batch_id = Column(Integer, ForeignKey("batches.batch_id"))
    department_id = Column(Integer, ForeignKey("departments.department_id"))
    password = Column(String(200), nullable=False)

    batch = relationship("Batch", back_populates="students")
    department = relationship("Department", back_populates="students")
    mentorships = relationship("Mentorship", back_populates="mentee")

class Event(Base):
    __tablename__ = "events"
    event_id = Column(Integer, primary_key=True, autoincrement=True)
    event_title = Column(String(255), nullable=False)
    event_date = Column(Date, nullable=False)
    event_description = Column(Text)
    created_by = Column(Integer, ForeignKey("alumni.alumni_id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    creator = relationship("Alumni", back_populates="events")

class Donation(Base):
    __tablename__ = "donations"
    donation_id = Column(Integer, primary_key=True, autoincrement=True)
    alumni_id = Column(Integer, ForeignKey("alumni.alumni_id"))
    amount = Column(Float, nullable=False)
    purpose = Column(String(255))
    date = Column(DateTime, default=datetime.utcnow)

    alumni = relationship("Alumni", back_populates="donations")

class Mentorship(Base):
    __tablename__ = "mentorships"
    mentor_id = Column(Integer, primary_key=True, autoincrement=True)
    alumni_id = Column(Integer, ForeignKey("alumni.alumni_id"))
    student_id = Column(Integer, ForeignKey("students.student_id"))
    status = Column(String(50), default="pending")
    requested_at = Column(DateTime, default=datetime.utcnow)

    mentor = relationship("Alumni", back_populates="mentorships")
    mentee = relationship("Student", back_populates="mentorships")

class Job(Base):
    __tablename__ = "jobs"
    job_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    posted_by = Column(Integer, ForeignKey("alumni.alumni_id"))
    deadline = Column(Date)

    poster = relationship("Alumni", back_populates="jobs")

# DB engine & session
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
