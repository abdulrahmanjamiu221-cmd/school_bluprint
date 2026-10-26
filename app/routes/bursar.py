from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.forms import PaymentForm
from app.models import Payment, Role, Student

bursar_bp = Blueprint("bursar", __name__)


@bursar_bp.route("/bursar/payments", methods=["GET", "POST"])
@login_required
def payments():
    if current_user.role not in {Role.BURSAR, Role.SCHOOL_ADMIN}:
        flash("Only a bursar or school admin can record payments.", "danger")
        return redirect(url_for("dashboard.dashboard"))

    form = PaymentForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(id=form.student_id.data, school_id=current_user.school_id).first()
        if not student:
            flash("Student not found in your school.", "danger")
            return render_template("payment_form.html", form=form)

        payment = Payment(
            school_id=current_user.school_id,
            student_id=student.id,
            reference=form.reference.data,
            amount=form.amount.data,
            method=form.method.data,
            status="verified",
            notes=form.notes.data,
        )
        db.session.add(payment)
        db.session.commit()
        flash("Payment recorded and verified.", "success")
        return redirect(url_for("bursar.payments"))

    payments_list = Payment.query.filter_by(school_id=current_user.school_id).all() if current_user.school_id else []
    return render_template("payment_form.html", form=form, payments=payments_list)
