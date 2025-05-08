from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import reverse

from . import views
from .models import Employee, User


# modelの単体テスト
class EmployeeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_employee_str_with_user(self):
        employee = Employee.objects.create(
            name="Alice", email="alice@example.com", department="HR", user=self.user
        )
        self.assertEqual(str(employee), "Alice (testuser)")

    def test_employee_str_without_user(self):
        employee = Employee.objects.create(
            name="Bob", email="bob@example.com", department="Finance"
        )
        self.assertEqual(str(employee), "Bob (No User)")


# VIEWの単体テスト
class EmployeeViewsUnitTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.staff_user = User.objects.create_user(
            username="staff", password="password", is_staff=True
        )
        self.user1 = User.objects.create_user(
            username="user1", password="testpass123", is_staff=True
        )
        self.user2 = User.objects.create_user(
            username="user2", password="testpass123", is_staff=False
        )
        self.employee1 = Employee.objects.create(
            user=self.user1, name="aiueo", email="aiueo@example.com", department="HR"
        )
        self.employee2 = Employee.objects.create(
            user=self.user2,
            name="kakikukeko",
            email="kakikukeko@example.com",
            department="HR",
        )

    # employee_new
    def test_employee_new_view_post_valid(self):
        data = {
            "name": "New Employee",
            "department": "HR",
            "email": "newemployee@example.com",
            "username": "newuser",
            "password": "newpassword01",
        }
        request = self.factory.post(reverse("employee_new"), data)
        request.user = self.staff_user
        response = views.employee_new(request)
        # POSTが有効なら302が通るはず
        self.assertEqual(response.status_code, 302)

    # employee_list
    def test_employee_list_view(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse("employee_index"))
        self.assertEqual(response.status_code, 200)

        content = response.content.decode("utf-8")

        self.assertIn("aiueo", content)
        self.assertIn("HR", content)
        self.assertIn("True", content)  # is_staffがTrue

        self.assertIn("kakikukeko", content)
        self.assertIn("HR", content)
        self.assertIn("False", content)  # is_staffがFalse


# 従業員編集画面の単体テスト
class EmployeeUpdateViewsUnitTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.staff_user = User.objects.create_user(
            username="staff", password="password", is_staff=True
        )
        self.user = User.objects.create_user(
            username="user1", password="testpass123", is_staff=True
        )
        self.employee = Employee.objects.create(
            user=self.user, name="Alice", email="alice@example.com", department="HR"
        )

        self.url = reverse("employee_edit", kwargs={'pk': self.employee.pk})

    # フォームの表示をテスト
    def test_get_update_view(self):

        self.client.login(username="staff", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alice")
        self.assertContains(response, "alice@example.com")

    # パスワードが空の場合のテスト
    def test_post_update_view(self):
        data = {
            "name": "Bob",
            "email": "bob@example.com",
            "username": "newUser1",
            "password": "",
        }
        self.client.login(username="staff", password="password")

        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('employee_index'))

        self.employee.refresh_from_db()
        self.user.refresh_from_db()

        self.assertEqual(self.employee.name, "Bob")
        self.assertEqual(self.employee.email, "bob@example.com")
        self.assertEqual(self.user.username, "newUser1")
        self.assertTrue(self.user.check_password('testpass123'))

    # パスワードが入力された場合のテスト
    def test_post_update_view_with_password(self):
        data = {
            "name": "Bob",
            "email": "bob@example.com",
            "username": "newUser1",
            "password": "newPassword01",
        }
        self.client.login(username="staff", password="password")

        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('employee_index'))

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newPassword01'))

    # パスワードが不適切な場合のテスト
    def test_post_update_view_with_password(self):
        data = {
            "name": "Bob",
            "email": "bob@example.com",
            "username": "newUser1",
            "password": "newPassword",
        }
        self.client.login(username="staff", password="password")

        response = self.client.post(self.url, data)
        self.assertContains(
            response, "パスワードは英数字を含む8文字以上にしてください。"
        )
