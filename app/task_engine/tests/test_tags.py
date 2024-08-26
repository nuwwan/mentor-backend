from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from app.utility import CONFIG_SAMPLE_TEST_USER
from authentication.utils import generate_jwt_token
from task_engine.models import Tag

AuthUser = get_user_model()

test_tag_payload = {"title": "testtag"}


class BaseTagTest(APITestCase):

    def setUp(self) -> None:
        test_user = AuthUser.objects.create_user(
            email=CONFIG_SAMPLE_TEST_USER.get("email"),
            password=CONFIG_SAMPLE_TEST_USER.get("password"),
            first_name=CONFIG_SAMPLE_TEST_USER.get("firstname"),
            last_name=CONFIG_SAMPLE_TEST_USER.get("lastname"),
        )
        self.user = test_user
        self.token = generate_jwt_token(test_user)
        return super().setUp()


class TestCreateTag(BaseTagTest):
    def __init__(self, methodName: str = "runTest") -> None:
        self.url = reverse("create_tag")
        super().__init__(methodName)

    def test_create_single_tag(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        # call backend
        response = self.client.post(self.url, test_tag_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("id"), 1)
        self.assertEqual(response.data.get("title"), test_tag_payload.get("title"))

    def test_create_tag_without_title(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        # call backend
        response = self.client.post(self.url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_tag_case_conversion(self):
        tag_payload = {"title": "Tag"}
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        # call backend
        response = self.client.post(self.url, tag_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("title"), tag_payload.get("title").lower())

    def test_create_tag_title_with_space(self):
        tag_payload = {"title": "ttest ag"}
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        # call backend
        response = self.client.post(self.url, tag_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
