from django.test import TestCase
from .models import DailyReportComment, DailyReport
from employees.models import Employee, User


# Create your tests here.


# modelの単体テスト
class DailyReportCommentTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.employee = Employee.objects.create(
            name="Alice", email="alice@example.com", department="HR", user=self.user
        )
        self.dailyReport = DailyReport.objects.create()

    def test_report_comment_str_with_user(self):
        daily_report_comment = DailyReportComment.objects.create(
            employee=self.employee,
            daily_report=self.dailyReport,
            comment="コメントです。",
        )
        self.assertEqual(str(daily_report_comment), "Alice (コメントです。)")
