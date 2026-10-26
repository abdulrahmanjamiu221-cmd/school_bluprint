import enum
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db


class Role(enum.Enum):
    SUPER_ADMIN = "super_admin"
    SCHOOL_ADMIN = "school_admin"
    PRINCIPAL = "principal"
    VICE_PRINCIPAL = "vice_principal"
    EXAMINATION_OFFICER = "examination_officer"
    TEACHER = "teacher"
    BURSAR = "bursar"
    PARENT = "parent"


class School(db.Model):
    __tablename__ = "schools"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.String(250), nullable=True)
    contact_email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    users = db.relationship("User", back_populates="school", cascade="all, delete-orphan")
    sessions = db.relationship("AcademicSession", back_populates="school", cascade="all, delete-orphan")
    students = db.relationship("Student", back_populates="school", cascade="all, delete-orphan")


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    role = db.Column(db.Enum(Role), nullable=False, default=Role.TEACHER)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    school = db.relationship("School", back_populates="users")
    teacher_assignments = db.relationship("TeacherAssignment", back_populates="teacher")
    result_entries = db.relationship("ResultEntry", back_populates="teacher")
    payments = db.relationship("Payment", back_populates="staff_member")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class AcademicSession(db.Model):
    __tablename__ = "academic_sessions"

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)

    school = db.relationship("School", back_populates="sessions")
    terms = db.relationship("AcademicTerm", back_populates="session", cascade="all, delete-orphan")


class AcademicTerm(db.Model):
    __tablename__ = "academic_terms"

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey("academic_sessions.id"), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)

    session = db.relationship("AcademicSession", back_populates="terms")


class SchoolClass(db.Model):
    __tablename__ = "school_classes"

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    level = db.Column(db.String(20), nullable=False)
    arm = db.Column(db.String(20), nullable=True)

    students = db.relationship("Student", back_populates="school_class")
    assignments = db.relationship("TeacherAssignment", back_populates="school_class")


class Subject(db.Model):
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    code = db.Column(db.String(40), nullable=True)

    assignments = db.relationship("TeacherAssignment", back_populates="subject")


class TeacherAssignment(db.Model):
    __tablename__ = "teacher_assignments"

    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey("school_classes.id"), nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"), nullable=False)

    teacher = db.relationship("User", back_populates="teacher_assignments")
    subject = db.relationship("Subject", back_populates="assignments")
    school_class = db.relationship("SchoolClass", back_populates="assignments")


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey("school_classes.id"), nullable=True)
    admission_number = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    photo_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    school = db.relationship("School", back_populates="students")
    school_class = db.relationship("SchoolClass", back_populates="students")
    records = db.relationship("ResultEntry", back_populates="student")
    payments = db.relationship("Payment", back_populates="student")

    __table_args__ = (
        db.UniqueConstraint("school_id", "admission_number", name="uq_school_admission_number"),
    )


class ResultEntry(db.Model):
    __tablename__ = "result_entries"

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey("school_classes.id"), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey("academic_sessions.id"), nullable=False)
    term_id = db.Column(db.Integer, db.ForeignKey("academic_terms.id"), nullable=False)
    ca = db.Column(db.Float, default=0)
    test = db.Column(db.Float, default=0)
    assignment = db.Column(db.Float, default=0)
    practical = db.Column(db.Float, default=0)
    exam = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)
    grade = db.Column(db.String(10), nullable=True)
    status = db.Column(db.String(30), default="draft")
    remarks = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    teacher = db.relationship("User", back_populates="result_entries")
    student = db.relationship("Student", back_populates="records")


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    reference = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    method = db.Column(db.String(40), nullable=False)
    status = db.Column(db.String(30), default="pending")
    verified_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship("Student", back_populates="payments")
    staff_member = db.relationship("User", back_populates="payments")


class ParentGuardian(db.Model):
    __tablename__ = "parent_guardians"

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    relationship = db.Column(db.String(50), nullable=True)


class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey("schools.id"), nullable=False)
    action = db.Column(db.String(150), nullable=False)
    details = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
