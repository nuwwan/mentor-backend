from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import AuthUser
from .utils import generate_jwt_token


class RegisterTestCases(APITestCase):
    """
    Test for success case: user creation with correct data.
    """

    def test_create_auth_user(self):
        url = reverse("register_view")
        data = {
            "email": "test_user@gmail.com",
            "password": "test",
            "firstname": "test",
            "lastname": "user",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AuthUser.objects.count(), 1)
        self.assertEqual(AuthUser.objects.get().first_name, "test")

    """
    Test for fail case 1: Duplicate user(email)
    """

    def test_user_already_exists(self):
        url = reverse("register_view")
        data = {
            "email": "test_user@gmail.com",
            "password": "test",
            "firstname": "test",
            "lastname": "user",
        }
        # create the user first
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # create again and assert for response code
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    """
    Test for fail case 2: when username is provided but not password
    """

    def test_payload_missing_password(self):
        url = reverse("register_view")
        data = {
            "email": "test_user@gmail.com",
            "firstname": "test",
            "lastname": "user",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    """
    Test for fail case 3: when username is not sent on payload
    """

    def test_payload_missing_username(self):
        url = reverse("register_view")
        data = {
            "password": "test",
            "firstname": "test",
            "lastname": "user",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    """
    Test for fail case 3: when username is not sent on payload
    """

    def test_payload_missing_firstname(self):
        url = reverse("register_view")
        data = {
            "email": "test_user@gmail.com",
            "password": "test",
            "lastname": "user",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTests(APITestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        self.email = "test_user@gmail.com"
        self.password = "test"
        self.first_name = "test"
        self.last_name = "user"
        self.url = reverse("login_view")
        super().__init__(methodName)

    def setUp(self) -> None:
        # 1. Create a user first
        user = AuthUser.objects.create_user(
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
        )

    """
    Success case: for all correct inputs
    """

    def test_login_username_and_password(self):
        data = {"email": self.email, "password": self.password}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    """
    Error case 1: when the un-registered user
    """

    def test_login_unregistered_user(self):
        data = {"email": "test_user1@gmail.com", "password": self.password}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    """
    Error case 2: when the password is wrong but username is correct
    """

    def test_login_wrong_password(self):
        data = {"email": self.email, "password": "wrong_password"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProtectedViewTests(APITestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        self.email = "test_user@gmail.com"
        self.password = "test"
        self.first_name = "test"
        self.last_name = "user"
        self.url = reverse("get_user")
        super().__init__(methodName)

    def setUp(self) -> None:
        # 1. Create a user first
        user = AuthUser.objects.create_user(
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
        )
        self.token = generate_jwt_token(user)

    """
    Success case
    """

    def test_for_valid_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
