from flask import Blueprint, render_template
from flask_login import current_user, login_required

from app.models import AcademicSession, Payment, ResultEntry, Role, Student, Subject, User

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    school = current_user.school
    total_students = Student.query.filter_by(school_id=school.id).count() if school else 0
    total_teachers = User.query.filter_by(school_id=school.id).filter(User.role == Role.TEACHER).count() if school else 0
    total_sessions = AcademicSession.query.filter_by(school_id=school.id).count() if school else 0
    total_subjects = Subject.query.filter_by(school_id=school.id).count() if school else 0
    total_payments = Payment.query.filter_by(school_id=school.id).count() if school else 0
    total_results = ResultEntry.query.filter_by(school_id=school.id).count() if school else 0

    return render_template(
        "dashboard.html",
        title="Dashboard",
        school=school,
        total_students=total_students,
        total_teachers=total_teachers,
        total_sessions=total_sessions,
        total_subjects=total_subjects,
        total_payments=total_payments,
        total_results=total_results,
    )
