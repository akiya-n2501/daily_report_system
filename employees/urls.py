from django.urls import path

from . import views
from .views import EmployeeListView

urlpatterns = [
    path("", EmployeeListView.as_view(), name="employee_index"),
    path("new/", views.employee_new, name="employee_new"),
    path("<int:pk>/edit/", views.EmployeeUpdateView.as_view(), name="employee_edit"),
    path(
        "<int:pk>/delete_confirm",
        views.employee_delete_confirm,
        name="employee_delete_confirm",
    ),
    path("<int:pk>/delete", views.employee_delete, name="employee_delete"),
]
