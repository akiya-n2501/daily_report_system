from django.test import TestCase
from .models import DailyReportComment, DailyReport
from employees.models import Employee, User
from django.test.client import RequestFactory
from django.urls import reverse

from . import views

import datetime


class DailyReportTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.employee = Employee.objects.create(
            name="Alice", email="alice@example.com", department="HR", user=self.user
        )

    def test_report_str_with_user(self):
        daily_report = DailyReport.objects.create(
            employee_code=self.employee,
            job_description="これは業務内容です。",
            reported_on=datetime.date.today(),
        )
        self.assertEqual(
            str(daily_report),
            f"Employee: Alice, Date: {datetime.date.today()}, Content: これは業務内容, CreatedAt: {daily_report.created_at}, UpdatedAt: {daily_report.updated_at}",
        )


# modelの単体テスト
class DailyReportCommentTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="testuser", password="password")
        self.user2 = User.objects.create_user(username="testuser2", password="password")
        self.employee = Employee.objects.create(
            name="Alice", email="alice@example.com", department="HR", user=self.user1
        )
        self.manager = Employee.objects.create(
            name="Bob", email="Bob@example.com", department="HR", user=self.user2
        )
        self.daily_report = DailyReport.objects.create(
            employee_code=self.employee,
            job_description="これは業務内容です。",
            reported_on=datetime.date.today(),
        )

    def test_report_comment_str_with_user(self):
        daily_report_comment = DailyReportComment.objects.create(
            employee_code=self.manager,
            daily_report_code=self.daily_report,
            comment="これはコメントです。",
        )
        self.assertEqual(
            str(daily_report_comment),
            f"Commenter: Bob, Employee: Alice, Date: {datetime.date.today()}, Comment: これはコメント, CreatedAt: {daily_report_comment.created_at}, UpdatedAt: {daily_report_comment.updated_at}",
        )


# VIEWの単体テスト
class DailyReportCommentViewsUnitTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user1 = User.objects.create_user(
            username="testuser", password="password", is_staff=True
        )
        self.user2 = User.objects.create_user(username="testuser2", password="password")
        self.employee = Employee.objects.create(
            name="Alice", email="alice@example.com", department="HR", user=self.user1
        )
        self.manager = Employee.objects.create(
            name="Bob", email="Bob@example.com", department="HR", user=self.user2
        )
        self.daily_report = DailyReport.objects.create(
            employee_code=self.employee,
            job_description="これは業務内容です。",
            reported_on=datetime.date.today(),
        )

    # employee_new
    def test_daily_report_comment_new_view_post_valid(self):
        data = {
            "comment": "これはコメントです。",
        }
        request = self.factory.post(
            reverse(
                "daily_report_comment_new", kwargs={"report_id": self.daily_report.pk}
            ),
            data,
        )

        request.user = self.user1
        response = views.DailyReportCommentCreateView.as_view()(request)
        # POSTが有効なら302が通るはず
        self.assertEqual(response.status_code, 302)
