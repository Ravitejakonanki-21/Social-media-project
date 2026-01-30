from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("posts", views.PostViewSet, basename="post")
router.register("comments", views.CommentViewSet, basename="comment")
router.register("profiles", views.UserProfileViewSet, basename="profile")
router.register("friend-requests", views.FriendRequestViewSet, basename="friendrequest")
router.register("follows", views.FollowViewSet, basename="follow")
router.register("notifications", views.NotificationViewSet, basename="notification")

urlpatterns = [
    path("", include(router.urls)),
]
