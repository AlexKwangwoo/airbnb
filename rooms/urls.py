from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("create/", views.CreateRoomView.as_view(), name="create"),
    path("<int:pk>", views.RoomDetail.as_view(), name="detail"),
    path("<int:pk>/edit/", views.EditRoomView.as_view(), name="edit"),
    path("<int:pk>/photos/", views.RoomPhotosView.as_view(), name="photos"),
    path("<int:pk>/photos/add", views.AddPhotoView.as_view(), name="add-photo"),
    path(
        "<int:room_pk>/photos/<int:photo_pk>/delete/",
        views.delete_photo,
        name="delete-photo",
    ),
    path(
        "<int:room_pk>/photos/<int:photo_pk>/edit/",
        views.EditPhotoView.as_view(),
        name="edit-photo",
    ),
    path("search/", views.SearchView.as_view(), name="search"),
]
# 룸의 view가 def에서 class로 바뀌면서.. HomeView class처럼 바뀐다!

# urlpatterns = [path("<int:pk>", views.room_detail, name="detail")]
# rooms/~~ 숫자가 <int:pk>가 된다!! 방의 id
# pk는 room_detail의 request, -> 다음 인자가 될것이다