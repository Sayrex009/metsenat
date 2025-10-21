from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView
from app.views import (
    AdminViewSet,
    UniversityViewSet,
    StudentViewSet,
    SponsorStudentViewSet,
    SponsorRegisterAPIView,
    AddStudentSponsorAPIView,
    DashboardSummaryAPIView,
    SponsorDetailAPIView,
    StudentDetailAPIView,
    SponsorListAPIVIew,
    SponsorDetailSerializer,
    DashboardChartAPIView,
)

router = DefaultRouter()
router.register("admins", AdminViewSet)
router.register("universities", UniversityViewSet)
router.register("students", StudentViewSet)
router.register("sponsor-students", SponsorStudentViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("api/", include(router.urls)),
    path('sponsor-register/', SponsorRegisterAPIView.as_view()),
    path('student_sponsor/', AddStudentSponsorAPIView.as_view()),
    path('dashboard_summary/', DashboardSummaryAPIView.as_view()),
    path('student/<int:pk>/', StudentDetailAPIView.as_view()),
    path('sponsors/', SponsorListAPIVIew.as_view()),
    path('sponsor/<int:pk>/', SponsorDetailAPIView.as_view()),
    path('dashboard_chart/', DashboardChartAPIView.as_view())
]
