from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("<int:pk>", views.RoomDetail.as_view(), name="detail"),
    path("search/", views.search, name="search"),
]
# 룸의 view가 def에서 class로 바뀌면서.. HomeView class처럼 바뀐다!

# urlpatterns = [path("<int:pk>", views.room_detail, name="detail")]
# rooms/~~ 숫자가 <int:pk>가 된다!! 방의 id
# pk는 room_detail의 request, -> 다음 인자가 될것이다