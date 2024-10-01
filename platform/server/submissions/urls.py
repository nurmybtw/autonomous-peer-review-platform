from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubmissionViewSet, ReviewRequestViewSet

submission_router = DefaultRouter()
submission_router.register(r'submissions', SubmissionViewSet)

revreq_router = DefaultRouter()
revreq_router.register(r'review_requests', ReviewRequestViewSet)

urlpatterns = [
    path('', include(submission_router.urls)),
    path('', include(revreq_router.urls)),
]
