from application.register_user.register_user_application_service import execute as execute_user_registration


def register_user(params, db):
    return execute_user_registration(params, db)