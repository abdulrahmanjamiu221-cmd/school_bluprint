from app.models import Role


def user_can_access_school(user, school_id):
    if user is None:
        return False
    if user.role == Role.SUPER_ADMIN:
        return True
    return user.school_id == school_id


def user_can_manage_results(user):
    return user.role in {Role.PRINCIPAL, Role.VICE_PRINCIPAL, Role.SCHOOL_ADMIN, Role.EXAMINATION_OFFICER, Role.TEACHER}
