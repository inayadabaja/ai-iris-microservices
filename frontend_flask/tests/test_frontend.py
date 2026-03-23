from unittest.mock import patch
from app import create_app, db


def get_client():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False
    })

    with app.app_context():
        db.create_all()

    return app.test_client()


def test_app_creation():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })
    assert app is not None


def test_home_route():
    client = get_client()
    response = client.get("/")
    assert response.status_code == 200


def test_signup_page():
    client = get_client()
    response = client.get("/signup")
    assert response.status_code == 200


def test_login_page():
    client = get_client()
    response = client.get("/login")
    assert response.status_code == 200


@patch("app.services.auth_service.AuthService.signup")
def test_signup_success(mock_signup):
    class MockUser:
        id = 1
        username = "inaya"

    mock_signup.return_value = MockUser()

    client = get_client()
    response = client.post(
        "/signup",
        data={
            "username": "inaya",
            "email": "inaya@test.com",
            "password": "123456"
        },
        follow_redirects=False
    )

    assert response.status_code in (302, 303)


@patch("app.services.auth_service.AuthService.login")
def test_login_success(mock_login):
    class MockUser:
        id = 1
        username = "inaya"

    mock_login.return_value = MockUser()

    client = get_client()
    response = client.post(
        "/login",
        data={
            "username": "inaya",
            "password": "123456"
        },
        follow_redirects=False
    )

    assert response.status_code in (302, 303)


def test_predict_requires_login():
    client = get_client()
    response = client.get("/predict", follow_redirects=False)
    assert response.status_code in (302, 303)


@patch("app.services.prediction_service.PredictionFrontendService.predict")
def test_predict_success(mock_predict):
    mock_predict.return_value = {
        "prediction_id": 1,
        "predicted_class": "setosa"
    }

    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })
    client = app.test_client()

    with client.session_transaction() as sess:
        sess["user_id"] = 1
        sess["username"] = "inaya"

    response = client.post(
        "/predict",
        data={
            "sepal_length": "5.1",
            "sepal_width": "3.5",
            "petal_length": "1.4",
            "petal_width": "0.2"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"setosa" in response.data


@patch("app.services.prediction_service.PredictionFrontendService.send_feedback")
def test_feedback_true_success(mock_feedback):
    mock_feedback.return_value = {
        "message": "Feedback saved successfully",
        "feedback_id": 1
    }

    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })
    client = app.test_client()

    with client.session_transaction() as sess:
        sess["user_id"] = 1
        sess["username"] = "inaya"

    response = client.post(
        "/feedback/1/true",
        data={"true_label": "setosa"},
        follow_redirects=False
    )

    assert response.status_code in (302, 303)