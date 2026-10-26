from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.models import Role, ResultEntry, Student

parent_bp = Blueprint("parent", __name__)


@parent_bp.route("/parent/results")
@login_required
def parent_results():
    if current_user.role != Role.PARENT:
        flash("This portal is for verified parents and guardians.", "danger")
        return redirect(url_for("dashboard.dashboard"))

    students = Student.query.filter_by(school_id=current_user.school_id).all() if current_user.school_id else []
    results = ResultEntry.query.filter_by(school_id=current_user.school_id).all() if current_user.school_id else []
    return render_template("parent_results.html", students=students, results=results)
