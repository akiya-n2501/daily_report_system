from django.urls import path

from . import views
from .views import DailyReportCommentCreateView

urlpatterns = [
    path(
        "<int:report_id>/comment/new/",
        DailyReportCommentCreateView.as_view(),
        name="employee_index",
    ),
]
