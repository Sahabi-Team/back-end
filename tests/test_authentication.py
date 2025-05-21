import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient
from authentication.views import RegisterView, LoginView, ChangePasswordView

pytestmark = pytest.mark.django_db  # Apply DB access to the whole module

User = get_user_model()

def prRed(skk): print("\033[91m {}\033[00m".format(skk))

def test_register_view_direct():
    factory = APIRequestFactory()
    request = factory.post('/api/auth/register/', {
        "name": "Test User",
        "username": "testuser123",
        "email": "test@example.com",
        "password": "securepass123",
        "phone_number": "09120000000",
        "role": "trainee"
    }, format='json')

    view = RegisterView.as_view()
    response = view(request)
    prRed(f"REGISTER RESPONSE: {response.status_code} {response.data}")
    assert response.status_code == 201


@pytest.fixture(scope="module")
def create_user(django_db_blocker):
    with django_db_blocker.unblock():
        def make_user(**kwargs):
            return User.objects.create_user(
                username=kwargs.get("username", "testuser123"),
                email=kwargs.get("email", "test@example.com"),
                password=kwargs.get("password", "securepass123"),
                name=kwargs.get("name", "Test User"),
                phone_number=kwargs.get("phone_number", "09120000000"),
                # role=kwargs.get("role", "trainee")
            )
        return make_user


def test_login_view_direct(create_user):
    user = create_user()
    factory = APIRequestFactory()
    request = factory.post('/api/auth/login/', {
        "username": "testuser123",
        "password": "securepass123"
    }, format='json')

    view = LoginView.as_view()
    response = view(request)
    # prRed(f"LOGIN RESPONSE: {response.status_code} {response.data}")
    assert response.status_code == 200
    # prRed(response)
    assert "access" in response.data['tokens']


@pytest.mark.django_db
def test_change_password_view_direct(create_user):
    user = create_user(username="user1", password="oldpass123")

    client = APIClient()

    login_response = client.post("/api/auth/login/", {
        "username": "user1",
        "password": "oldpass123",

    }, format="json")
    assert login_response.status_code == 200
    access_token = login_response.data["tokens"]["access"]

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    response = client.post("/api/auth/change-password/", {
        "old_password": "oldpass123",
        "new_password": "newpass456",
        "confirm_password":"newpass456"
    }, format="json")

    # print("CHANGE PASSWORD RESPONSE:", response.data)

    assert response.status_code == 200
    assert response.data["message"] == "Password updated successfully."
    user.refresh_from_db()
    assert user.check_password("newpass456")