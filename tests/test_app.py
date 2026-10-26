from app import create_app


def test_app_login_and_dashboard():
    app = create_app({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    client = app.test_client()
    response = client.get("/login")
    assert response.status_code == 200
    assert b"SchoolResult Pro" in response.data

    response = client.post(
        "/login",
        data={"email": "admin@schoolresultpro.com", "password": "admin123"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Dashboard" in response.data
