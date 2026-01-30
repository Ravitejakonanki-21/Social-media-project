from django.urls import path
from . import views

app_name = "friends"
urlpatterns = [
    path("", views.friend_list_view, name="list"),
    path("send/<str:username>/", views.send_friend_request_view, name="send"),
    path("accept/<int:pk>/", views.accept_friend_request_view, name="accept"),
    path("follow/<str:username>/", views.follow_view, name="follow"),
    path("unfollow/<str:username>/", views.unfollow_view, name="unfollow"),
]
