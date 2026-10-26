from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.forms import SchoolForm, StudentForm
from app.models import Role, School, SchoolClass, Student, User

school_bp = Blueprint("school", __name__)


@school_bp.route("/schools/new", methods=["GET", "POST"])
@login_required
def create_school():
    if current_user.role != Role.SUPER_ADMIN:
        flash("Only the super administrator can create school accounts.", "danger")
        return redirect(url_for("dashboard.dashboard"))

    form = SchoolForm()
    if form.validate_on_submit():
        school = School(
            name=form.name.data,
            code=form.code.data,
            address=form.address.data,
            contact_email=form.contact_email.data,
            phone=form.phone.data,
        )
        db.session.add(school)
        db.session.commit()
        flash("School account created successfully.", "success")
        return redirect(url_for("dashboard.dashboard"))
    return render_template("school_form.html", form=form)


@school_bp.route("/students/new", methods=["GET", "POST"])
@login_required
def create_student():
    if current_user.role not in {Role.SCHOOL_ADMIN, Role.PRINCIPAL}:
        flash("You are not authorized to register students.", "danger")
        return redirect(url_for("dashboard.dashboard"))

    form = StudentForm()
    if form.validate_on_submit():
        school = current_user.school
        if not school:
            flash("Your account is not linked to a school.", "danger")
            return redirect(url_for("dashboard.dashboard"))

        student = Student(
            school_id=school.id,
            class_id=form.class_id.data,
            admission_number=form.admission_number.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            gender=form.gender.data,
        )
        db.session.add(student)
        try:
            db.session.commit()
            flash("Student registered successfully.", "success")
            return redirect(url_for("dashboard.dashboard"))
        except Exception:
            db.session.rollback()
            flash("This admission number may already exist for the school.", "danger")

    classes = SchoolClass.query.filter_by(school_id=current_user.school_id).all() if current_user.school_id else []
    return render_template("student_form.html", form=form, classes=classes)
