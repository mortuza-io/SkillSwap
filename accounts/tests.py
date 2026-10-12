from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AuthenticationTests(TestCase):
    def setUp(self):
        self.data = {
            "full_name": "Alex Taylor",
            "username": "alex",
            "email": "alex@example.com",
            "password1": "LearningTogether!842",
            "password2": "LearningTogether!842",
        }

    def test_signup_hashes_password_and_logs_in(self):
        response = self.client.post(reverse("signup"), self.data)
        self.assertRedirects(response, reverse("home"))
        user = get_user_model().objects.get(username="alex")
        self.assertTrue(user.check_password(self.data["password1"]))
        self.assertNotEqual(user.password, self.data["password1"])
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)

    def test_signup_rejects_duplicate_username_and_email(self):
        self.client.post(reverse("signup"), self.data)
        self.client.logout()
        response = self.client.post(reverse("signup"), self.data)
        self.assertIn("username", response.context["form"].errors)
        self.assertIn("email", response.context["form"].errors)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_signup_rejects_mismatched_passwords(self):
        self.data["password2"] = "DifferentPassword!93"
        response = self.client.post(reverse("signup"), self.data)
        self.assertIn("password2", response.context["form"].errors)
        self.assertFalse(get_user_model().objects.exists())

    def test_home_requires_login(self):
        self.assertRedirects(self.client.get(reverse("home")), "/login/?next=/")

    def test_login_and_post_logout(self):
        get_user_model().objects.create_user(
            username="alex", email="alex@example.com", password=self.data["password1"]
        )
        bad = self.client.post(reverse("login"), {"username": "alex", "password": "wrong"})
        self.assertTrue(bad.context["form"].errors)
        response = self.client.post(reverse("login"), {"username": "alex", "password": self.data["password1"]})
        self.assertRedirects(response, reverse("home"))
        self.assertEqual(self.client.get(reverse("logout")).status_code, 405)
        self.assertRedirects(self.client.post(reverse("logout")), reverse("login"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_login_does_not_redirect_to_external_site(self):
        get_user_model().objects.create_user(username="alex", email="alex@example.com", password=self.data["password1"])
        response = self.client.post(reverse("login"), {
            "username": "alex", "password": self.data["password1"], "next": "https://example.com/",
        })
        self.assertRedirects(response, reverse("home"))

    def test_signup_requires_csrf_token(self):
        from django.test import Client

        response = Client(enforce_csrf_checks=True).post(reverse("signup"), self.data)
        self.assertEqual(response.status_code, 403)
