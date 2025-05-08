from django.test import TestCase
from django.urls import reverse, resolve
from ..views import DailyReportEditView

class TestUrls(TestCase):
    def test_post_index_url(self):
        view = resolve('/daily_reports/1/edit/')
        self.assertEqual(view.func.view_class, DailyReportEditView)