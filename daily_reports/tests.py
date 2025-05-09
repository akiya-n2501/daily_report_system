import datetime

from django.test import TestCase
from django.test.client import RequestFactory
from django.urls import resolve, reverse

from employees.models import Employee, User

from . import views
from .models import DailyReport, DailyReportComment
from .views import DailyReportCreateView

# # 日報新規登録画面の単体テスト
# class DailyReportCreateViewTest(TestCase):

#     def setUp(self):
#         self.factory = RequestFactory()
#         self.user = User.objects.create_user(username="testuser", password="password")
#         self.employee = Employee.objects.create(
#             name="Alice", email="alice@example.com", department="HR", user=self.user
#         )

#     def test_daily_report_new_view_post_valid(self):
#         data = {
#             "employee_code": self.employee,
#             "job_description": "これは業務内容です。",
#             "reported_on": datetime.date.today(),
#         }
#         request = self.factory.post(reverse("daily_report_new"), data)
#         request.user = self.user
#         response = DailyReportCreateView.as_view(request)

#         # フォームのエラーを確認
#         if response.status_code == 200:
#             print(response.context_data['form'].errors)
#         # POSTが有効なら302が通るはず
#         self.assertEqual(response.status_code, 302)
#         self.assertTrue(DailyReport.objects.filter(employee_code='A').exists())
#         # オブジェクトが存在することを確認


# class DailyReportCreateViewTest(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.user1 = User.objects.create_user(
#             username="testuser", password="password", is_staff=True
#         )
#         self.user2 = User.objects.create_user(username="testuser2", password="password")
#         self.employee = Employee.objects.create(
#             name="Alice", email="alice@example.com", department="HR", user=self.user1
#         )
#         self.manager = Employee.objects.create(
#             name="Bob", email="Bob@example.com", department="HR", user=self.user2
#         )
#         self.daily_report = DailyReport.objects.create(
#             employee_code=self.employee,
#             job_description="これは業務内容です。",
#             reported_on=datetime.date.today(),
#         )
#     # 日報新規作成のテスト
#     def test_daily_report_new_view_post_valid(self):
#         data = {
#             "job_description": "これは業務内容です。",
#         }
#         url = reverse(
#             "daily_report_new", kwargs={"report_id": self.daily_report.pk}
#         )
#         request = self.factory.post(url, data)

#         request.user = self.user1
#         response = views.DailyReportCreateView.as_view()(
#             request, report_id=self.daily_report.pk
#         )
#         # POSTが有効なら302が通るはず
#         self.assertEqual(response.status_code, 302)

#     # 日報が作られていることを確認するテスト
#     def test_daily_report_new_view_post_created(self):
#         data = {
#             "job_description": "これは業務内容です。",
#         }
#         url = reverse(
#             "daily_report_new", kwargs={"report_id": self.daily_report.pk}
#         )
#         request = self.factory.post(url, data)

#         request.user = self.user1
#         response = views.DailyReportCreateView.as_view()(
#             request, report_id=self.daily_report.pk
#         )

#         self.assertEqual(DailyReport.objects.count(), 1)

#         comment = DailyReport.objects.first()
#         self.assertEqual(DailyReport.employee_code, self.employee)


#     # 日報のフォームが空の時のテスト
#     def test_daily_report_invalid_form(self):
#         data = {"job_description": ""}
#         url = reverse(
#             "daily_report_new", kwargs={"report_id": self.daily_report.pk}
#         )
#         self.client.login(username="testuser", password="password")
#         response = self.client.post(url, data)

#         self.assertEqual(response.status_code, 200)


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


# 日報コメント新規作成画面のテスト
class DailyReportCommentCreateViewUnitTest(TestCase):
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

    # 日報コメント新規作成のテスト
    def test_daily_report_comment_new_view_post_valid(self):
        data = {
            "comment": "これはコメントです。",
        }
        url = reverse("daily_report_comment_new", kwargs={"pk": self.daily_report.pk})
        request = self.factory.post(url, data)

        request.user = self.user1
        response = views.DailyReportCommentCreateView.as_view()(
            request, pk=self.daily_report.pk
        )
        # POSTが有効なら302が通るはず
        self.assertEqual(response.status_code, 302)

    # 日報コメントが作られていることを確認するテスト
    def test_daily_report_comment_new_view_post_created(self):
        data = {
            "comment": "これはコメントです。",
        }
        url = reverse("daily_report_comment_new", kwargs={"pk": self.daily_report.pk})
        request = self.factory.post(url, data)

        request.user = self.user1
        response = views.DailyReportCommentCreateView.as_view()(
            request, pk=self.daily_report.pk
        )

        self.assertEqual(DailyReportComment.objects.count(), 1)

        comment = DailyReportComment.objects.first()
        self.assertEqual(comment.comment, "これはコメントです。")
        self.assertEqual(comment.employee_code, self.employee)
        self.assertEqual(comment.daily_report_code, self.daily_report)

    # 日報コメントのフォームが空の時のテスト
    def test_daily_report_comment_invalid_form(self):
        data = {"comment": ""}
        url = reverse("daily_report_comment_new", kwargs={"pk": self.daily_report.pk})
        self.client.login(username="testuser", password="password")
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "コメントは1文字以上で入力してください。")


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

        self.user1 = User.objects.create_user(username="testuser1", password="password")
        self.employee1 = Employee.objects.create(
            name="Alice1", email="alice1@example.com", department="HR", user=self.user1
        )
        DailyReport.objects.create(
            reported_on="2010-01-01",
            employee_code=self.employee1,
            job_description="LGTM",
        )
        self.user2 = User.objects.create_user(username="testuser2", password="password")
        self.employee2 = Employee.objects.create(
            name="Alice2", email="alice2@example.com", department="HR2", user=self.user2
        )
        DailyReport.objects.create(
            reported_on="2025-05-08",
            employee_code=self.employee2,
            job_description="Sharingday",
        )
        self.user3 = User.objects.create_user(username="testuser3", password="password")
        self.employee3 = Employee.objects.create(
            name="Alice3", email="alice3@example.com", department="HR3", user=self.user3
        )
        DailyReport.objects.create(
            reported_on="2025-05-08",
            employee_code=self.employee3,
            job_description="Bunquet",
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

    def test_daily_report_search_without_login(self):
        # ログインしていない時にリダイレクトされるか
        response = self.client.get(reverse("daily_report_index"), {"keyword": "LGTM"})
        self.assertEqual(response.status_code, 302)

    def test_daily_report_search_with_employee_name(self):
        # 名前を検索し、含まれるべき日報が含まれるか
        self.client.force_login(self.user1)
        response = self.client.get(reverse("daily_report_index"), {"keyword": "Alice1"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alice1")
        self.assertNotContains(response, "Alice2")
        self.assertNotContains(response, "Alice3")
