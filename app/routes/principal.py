from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.models import Role, ResultEntry

principal_bp = Blueprint("principal", __name__)


@principal_bp.route("/principal/review")
@login_required
def review_results():
    if current_user.role not in {Role.PRINCIPAL, Role.VICE_PRINCIPAL, Role.EXAMINATION_OFFICER, Role.SCHOOL_ADMIN}:
        flash("You do not have permission to review results.", "danger")
        return redirect(url_for("dashboard.dashboard"))

    results = ResultEntry.query.filter_by(school_id=current_user.school_id).all() if current_user.school_id else []
    return render_template("principal_review.html", results=results)


@principal_bp.route("/principal/review/<int:result_id>/approve")
@login_required
def approve_result(result_id):
    if current_user.role not in {Role.PRINCIPAL, Role.SCHOOL_ADMIN}:
        flash("Only the principal or school admin can approve results.", "danger")
        return redirect(url_for("dashboard.dashboard"))

    result = ResultEntry.query.get_or_404(result_id)
    result.status = "approved"
    result.remarks = (result.remarks or "") + " | Approved by principal"
    result.teacher_id = result.teacher_id
    result.total = result.total or 0

    from app.extensions import db

    db.session.commit()
    flash("Result approved successfully.", "success")
    return redirect(url_for("principal.review_results"))
