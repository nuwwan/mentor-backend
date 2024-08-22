from django.urls import reverse
from django.contrib.auth import get_user_model
from authentication.utils import generate_jwt_token
from rest_framework import status
from rest_framework.test import APITestCase
from task_engine.models import Timeline, Mentorship
from app.utility import CONFIG_SAMPLE_TEST_USER, CONFIG_SAMPLE_TEST_USER_MENTOR

AuthUser = get_user_model()

"""
Test timeline Base view
"""
timeline_payload = {"title": "Timeline 1", "subject": "fin", "privacy": "pub"}


class BaseTestTimeline(APITestCase):
    def setUp(self) -> None:
        # create test user
        test_user = AuthUser.objects.create_user(
            email=CONFIG_SAMPLE_TEST_USER.get("email"),
            password=CONFIG_SAMPLE_TEST_USER.get("password"),
            first_name=CONFIG_SAMPLE_TEST_USER.get("firstname"),
            last_name=CONFIG_SAMPLE_TEST_USER.get("lastname"),
        )
        self.user = test_user
        self.token = generate_jwt_token(test_user)

        # create mentor
        test_user_mentor = AuthUser.objects.create_user(
            email=CONFIG_SAMPLE_TEST_USER_MENTOR.get("email"),
            password=CONFIG_SAMPLE_TEST_USER_MENTOR.get("password"),
            first_name=CONFIG_SAMPLE_TEST_USER_MENTOR.get("firstname"),
            last_name=CONFIG_SAMPLE_TEST_USER_MENTOR.get("lastname"),
        )
        self.mentor = test_user_mentor
        self.mentor_token = generate_jwt_token(test_user_mentor)

        return super().setUp()


"""
Get all Timelines for a user
"""


class TestTimelineList(BaseTestTimeline):
    def __init__(self, methodName: str = "runTest") -> None:
        self.url = reverse("timeline_list")
        super().__init__(methodName)

    def test_create_timeline(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        response = self.client.post(self.url, timeline_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_user_timeline(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        # Create timelines first
        Timeline.objects.create(
            title=timeline_payload.get("title"),
            user=self.user,
            subject=timeline_payload.get("subject"),
            privacy=timeline_payload.get("privacy"),
        )

        # Test the get timelines
        response = self.client.get(self.url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class TestTimelineDetail(BaseTestTimeline):
    def __init__(self, methodName: str = "runTest") -> None:
        self.url = reverse("timeline_detail", kwargs={"pk": 1})
        super().__init__(methodName)

    def test_get_timeline_detail(self):
        # Authenticate the user
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        # Create a timeline object
        Timeline.objects.create(
            title=timeline_payload.get("title"),
            user=self.user,
            subject=timeline_payload.get("subject"),
            privacy=timeline_payload.get("privacy"),
        )

        # Get the timeline where id=1
        response = self.client.get(self.url, format="json")
        response_timeline = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_timeline.get("title"), "Timeline 1")

    def test_update_timeline_detail(self):
        # Authenticate the user
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        # Create a timeline object
        Timeline.objects.create(
            title=timeline_payload.get("title"),
            user=self.user,
            subject=timeline_payload.get("subject"),
            privacy=timeline_payload.get("privacy"),
        )

        # update the timeline where id=1
        new_data = {**timeline_payload, "title": "Timeline 2"}
        response = self.client.put(self.url, new_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("title"), new_data.get("title"))

    def test_patch_timeline_detail(self):
        # Authenticate the user
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        # Create a timeline object
        Timeline.objects.create(
            title=timeline_payload.get("title"),
            user=self.user,
            subject=timeline_payload.get("subject"),
            privacy=timeline_payload.get("privacy"),
        )

        # update the timeline where id=1
        new_data = {"title": "Timeline 2"}
        response = self.client.patch(self.url, new_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("title"), new_data.get("title"))

    def test_remove_timeline_detail(self):
        # Authenticate the user
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        # Create a timeline object
        Timeline.objects.create(
            title=timeline_payload.get("title"),
            user=self.user,
            subject=timeline_payload.get("subject"),
            privacy=timeline_payload.get("privacy"),
        )
        # remove the timeline where id=1
        response = self.client.delete(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestAssignTimelineToMentor(BaseTestTimeline):
    def __init__(self, methodName: str = "runTest") -> None:
        self.url = reverse("add_mentor_to_timeline")
        super().__init__(methodName)

    def test_post_assign_timeline_to_mentor(self):
        # Authenticate the user
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        # create a timeline
        timeline = Timeline.objects.create(
            title=timeline_payload.get("title"),
            user=self.user,
            subject=timeline_payload.get("subject"),
            privacy=timeline_payload.get("privacy"),
        )

        # assign mentor
        mentor_data_payload = {
            "mentor": self.mentor.id,
            "timeline": timeline.id,
            "subject": "fin",
        }
        response = self.client.post(self.url, mentor_data_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_mentor_does_not_exists(self):
        # Authenticate the user
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        # create a timeline
        timeline = Timeline.objects.create(
            title=timeline_payload.get("title"),
            user=self.user,
            subject=timeline_payload.get("subject"),
            privacy=timeline_payload.get("privacy"),
        )

        strage_mentor_id = 123
        # assign mentor
        mentor_data_payload = {
            "mentor": strage_mentor_id,
            "timeline": timeline.id,
            "subject": "fin",
        }
        response = self.client.post(self.url, mentor_data_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_timeline_does_not_exists(self):
        # Authenticate the user
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        strage_timeline_id = 123
        # assign mentor
        mentor_data_payload = {
            "mentor": self.mentor.id,
            "timeline": strage_timeline_id,
            "subject": "fin",
        }
        response = self.client.post(self.url, mentor_data_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_incorrect_payload(self):
        # Authenticate the user
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        # create a timeline
        timeline = Timeline.objects.create(
            title=timeline_payload.get("title"),
            user=self.user,
            subject=timeline_payload.get("subject"),
            privacy=timeline_payload.get("privacy"),
        )

        # assign mentor
        mentor_data_payload = {
            "mentor": self.mentor.id,
            "timeline": timeline.id,
        }
        response = self.client.post(self.url, mentor_data_payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)


class TestGetTimelineForMentor(BaseTestTimeline):
    def __init__(self, methodName: str = "runTest") -> None:
        self.url = reverse("get_mentoring_timeline_for_mentor")
        super().__init__(methodName)

    def test_get_mentor_timelines(self):
        # Authenticate the user
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.mentor_token)

        # create a timeline
        timeline = Timeline.objects.create(
            title=timeline_payload.get("title"),
            subject=timeline_payload.get("subject"),
            privacy=timeline_payload.get("privacy"),
            user=self.user,
        )

        # assign mentor
        Mentorship.objects.create(
            mentor=self.mentor, mentee=self.user, timeline=timeline, subject="fin"
        )

        # get mentor timelines
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_mentor_timelines_for_no_records(self):
        # Authenticate the user
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.mentor_token)

        # get mentor timelines
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
