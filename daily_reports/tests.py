import datetime

from django.test import TestCase
from django.urls import reverse

from employees.models import Employee, User

from .models import DailyReport, DailyReportComment


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


# 日報一覧画面の単体テスト
class DailyReportListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.employee = Employee.objects.create(
            name="Alice", email="alice@example.com", department="HR", user=self.user
        )
        self.daily_report = DailyReport.objects.create(
            reported_on=datetime.date.today(),
            employee_code=self.employee,
            job_description="""
            所感
            ・コードレビューのときのLGTM等の用語について学んだので、実行する。
            ・チーム開発のGit/GitHubの運用ルールが無くて苦労したので、次回作成する。
            """,
        )

    def test_daily_report_list_view(self):
        # ログイン
        self.client.force_login(self.user)
        response = self.client.get(reverse("daily_report_index"))
        self.assertEqual(response.status_code, 200)

        content = response.content.decode("utf-8")

        self.assertIn(datetime.date.today().strftime("%Y/%m/%d"), content)
        # 従業員名
        self.assertIn(self.daily_report.employee_code.name, content)
        # 先頭10文字
        self.assertIn(self.daily_report.job_description[:10], content)


# 日報一覧画面の検索機能のテスト
class DailyReportSearchViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="testuser1", password="password")
        self.employee1 = Employee.objects.create(
            name="Alice", email="alice@example.com", department="HR", user=self.user1
        )
        DailyReport.objects.create(
            reported_on=datetime.date.today(),
            employee_code=self.employee1,
            job_description="LGTM",
        )
        self.user2 = User.objects.create_user(username="testuser2", password="password")
        self.employee2 = Employee.objects.create(
            name="Alice2", email="alice2@example.com", department="HR2", user=self.user2
        )
        DailyReport.objects.create(
            reported_on=datetime.date.today(),
            employee_code=self.employee2,
            job_description="Sharingday",
        )

    def test_daily_report_search(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse("search_list"), {"q": "LGTM"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "LGTM")
        self.assertNotContains(response, "Sharingday")
