from django.test import TestCase
from django.contrib.auth.models import User
from .models import Clinic, FollowUp, PublicViewLog, UserProfile


class FollowUpTests(TestCase):
    def setUp(self):
        self.clinic = Clinic.objects.create(name="Test Clinic")

        self.user = User.objects.create_user(
            username="testuser",
            password="testpass"
        )

        UserProfile.objects.create(
            user=self.user,
            clinic=self.clinic
        )

    def test_clinic_code_is_generated(self):
        self.assertTrue(self.clinic.clinic_code)

    def test_public_token_is_generated(self):
        followup = FollowUp.objects.create(
            clinic=self.clinic,
            created_by=self.user,
            patient_name="Patient A",
            phone="12345678",
            language="en",
            due_date="2026-01-01",
        )

        self.assertTrue(followup.public_token)

    def test_dashboard_requires_login(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)

    def test_user_cannot_access_other_clinic_followup(self):
        other_clinic = Clinic.objects.create(name="Other Clinic")

        other_user = User.objects.create_user(
            username="otheruser",
            password="pass"
        )

        UserProfile.objects.create(
            user=other_user,
            clinic=other_clinic
        )

        followup = FollowUp.objects.create(
            clinic=other_clinic,
            created_by=other_user,
            patient_name="Other Patient",
            phone="87654321",
            language="en",
            due_date="2026-01-02",
        )

        self.client.login(username="testuser", password="testpass")
        response = self.client.get(f"/{followup.pk}/edit/")

        self.assertIn(response.status_code, [403, 404])

    def test_public_view_creates_log(self):
        followup = FollowUp.objects.create(
            clinic=self.clinic,
            created_by=self.user,
            patient_name="Patient B",
            phone="12345678",
            language="en",
            due_date="2026-01-03",
        )

        self.client.get(f"/p/{followup.public_token}/")

        self.assertEqual(PublicViewLog.objects.count(), 1)
