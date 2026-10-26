from flask import Flask, redirect, url_for

from app.config import Config
from app.extensions import csrf, db, login_manager, migrate


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.school import school_bp
    from app.routes.teacher import teacher_bp
    from app.routes.principal import principal_bp
    from app.routes.bursar import bursar_bp
    from app.routes.parent import parent_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(school_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(principal_bp)
    app.register_blueprint(bursar_bp)
    app.register_blueprint(parent_bp)

    @app.route("/")
    def index():
        return redirect(url_for("auth.login"))

    with app.app_context():
        db.create_all()
        seed_demo_data()

    return app


def seed_demo_data():
    from app.models import AcademicSession, AcademicTerm, Role, School, User

    if School.query.count() == 0:
        school = School(
            name="New Bussa Academy",
            code="NBA",
            address="New Bussa, Niger State",
            contact_email="admin@schoolresultpro.com",
            phone="08030000000",
        )
        db.session.add(school)
        db.session.flush()

        session = AcademicSession(school_id=school.id, name="2026/2027", is_active=True)
        db.session.add(session)
        db.session.flush()

        term = AcademicTerm(school_id=school.id, session_id=session.id, name="First Term", is_active=True)
        db.session.add(term)

        admin = User(
            school_id=school.id,
            email="admin@schoolresultpro.com",
            full_name="Super Administrator",
            role=Role.SUPER_ADMIN,
        )
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()

    if User.query.filter_by(email="admin@schoolresultpro.com").count() == 0:
        school = School.query.first()
        admin = User(
            school_id=school.id,
            email="admin@schoolresultpro.com",
            full_name="Super Administrator",
            role=Role.SUPER_ADMIN,
        )
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
