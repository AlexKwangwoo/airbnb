from django.urls import path
from . import views

app_name = "reservations"

urlpatterns = [
    path(
        "create/<int:room>/<int:year>-<int:month>-<int:day>",
        views.create,
        name="create",
    ),
    path("<int:pk>/", views.ReservationDetailView.as_view(), name="detail"),
    path("<int:pk>/<str:verb>", views.edit_reservation, name="edit"),
    path("<int:pk>/delete/", views.delete_reservation, name="delete"),
    path(
        "reservationList/",
        views.ReservationListView.as_view(),
        name="reservation-list",
    ),
    path(
        "reservationList_host/",
        views.ReservationListHostView.as_view(),
        name="reservation-list-host",
    ),
]
