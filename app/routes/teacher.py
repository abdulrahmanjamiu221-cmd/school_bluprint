from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.forms import ResultEntryForm
from app.models import Role, ResultEntry, SchoolClass, Subject, TeacherAssignment

teacher_bp = Blueprint("teacher", __name__)


@teacher_bp.route("/teacher/results")
@login_required
def results():
    if current_user.role != Role.TEACHER:
        flash("This page is only for subject teachers.", "danger")
        return redirect(url_for("dashboard.dashboard"))

    assignments = TeacherAssignment.query.filter_by(teacher_id=current_user.id).all()
    return render_template("teacher_results.html", assignments=assignments)


@teacher_bp.route("/teacher/results/<int:assignment_id>", methods=["GET", "POST"])
@login_required
def grade_assignment(assignment_id):
    if current_user.role != Role.TEACHER:
        flash("Only teachers can enter scores.", "danger")
        return redirect(url_for("dashboard.dashboard"))

    assignment = TeacherAssignment.query.get_or_404(assignment_id)
    form = ResultEntryForm()
    if form.validate_on_submit():
        data = {
            "school_id": current_user.school_id,
            "teacher_id": current_user.id,
            "subject_id": assignment.subject_id,
            "class_id": assignment.class_id,
            "session_id": 1,
            "term_id": 1,
            "ca": form.ca.data or 0,
            "test": form.test.data or 0,
            "assignment": form.assignment.data or 0,
            "practical": form.practical.data or 0,
            "exam": form.exam.data or 0,
            "remarks": form.remarks.data,
        }
        total = sum(value for value in data.values() if isinstance(value, (int, float)))
        data["total"] = total
        data["grade"] = "A" if total >= 75 else "B" if total >= 65 else "C" if total >= 55 else "D" if total >= 45 else "F"
        data["status"] = "submitted"
        result = ResultEntry(**data)
        db.session.add(result)
        db.session.commit()
        flash("Scores saved and submitted for review.", "success")
        return redirect(url_for("teacher.results"))

    return render_template("result_form.html", form=form, assignment=assignment)
