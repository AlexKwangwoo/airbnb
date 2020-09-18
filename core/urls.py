# config url page!!!
from django.urls import path
from rooms import views as room_views

app_name = "core"  # config의 namespace

urlpatterns = [
    path("", room_views.HomeView.as_view(), name="home")
    # Homeview는 view로 전환해주는 메소드가 있다
    # path("", room_views.all_rooms, name="home"),  # "" 의 이미는 / 이다!
    # 장고가 볼때 장고가 url config가서 core url을 보고 온다!
]