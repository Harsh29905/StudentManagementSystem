from rest_framework.routers import DefaultRouter
from .viewsets import StudentViewSet
from django.urls import path
from . import views

router = DefaultRouter()
router.register(
    r"api/v3/students",
    StudentViewSet,
    basename="student-v3"
)

urlpatterns = [
    path("update/<int:id>/", views.student_update, name="student_update"),
    path("delete/<int:id>/", views.student_delete, name="student_delete"),
    path("api/students/", views.student_api_list, name="student_api_list"),
    path("api/students/create/", views.student_api_create, name="student_api_create"),
    path("api/students/<int:id>/", views.student_api_detail, name="student_api_detail"),
    path("api/students/<int:id>/update/", views.student_api_update, name="student_api_update"),
    path("api/students/<int:id>/partial_update/", views.student_api_partial_update, name="student_api_partial_update"),
    path("api/students/<int:id>/delete/",views.student_api_delete,name="student_api_delete"),
    path(
    "api/v2/students/",
    views.StudentListCreateAPI.as_view(),
    name="student_list_create_api"),
    path(
        "api/v2/students/<int:id>/",
        views.StudentDetailAPI.as_view(),
        name="student_detail_api"
    ),
    path("", views.home, name="home"),
    path("dashboard/", views.student_dashboard, name="student_dashboard"),
    path("list/", views.student_list, name="student_list"),
    path("add/", views.student_create, name="student_create"),
    path("courses/", views.course_list, name="course_list"),
    path("reports/", views.reports, name="reports"),
    path("register/", views.register, name="register"),
    
]
urlpatterns += router.urls