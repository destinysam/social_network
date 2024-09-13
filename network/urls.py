
from django.urls import path
from .views import ListUserAPI,SendFriendRequestAPI,UpdateFriendRequestAPI,AcceptedFriendRequestAPI,PendingFriendRequestAPI
from django_ratelimit.decorators import ratelimit
urlpatterns = [
    path("listusers/",ListUserAPI.as_view(),name="list-users"),
    path("send-friend-request/",ratelimit(key="user_or_ip",method="POST",rate="3/m")(SendFriendRequestAPI.as_view()),name="friend-request"),
    path("update-friend-request/<int:friend_request_id>/",UpdateFriendRequestAPI.as_view(),name="update-friend-request"),
    path("accepted-friend-requests/",AcceptedFriendRequestAPI.as_view(),name="accepted-friend-requests"),
    path("pending-friend-requests/",PendingFriendRequestAPI.as_view(),name="pending-friend-requests"),
]