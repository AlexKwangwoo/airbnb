"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# from . import setting 장고는 세팅을 불러올대 이렇게 하면 안됨!!


urlpatterns = [
    path("", include("core.urls", namespace="core")),
    path("rooms/", include("rooms.urls", namespace="rooms")),
    # http://localhost:8000/rooms/34 저기서 path("rooms/" ==> 8000/rooms/ 가 된다
    path("users/", include("users.urls", namespace="users")),
    path("reservations/", include("reservations.urls", namespace="reservations")),
    path(
        "admin/",
        admin.site.urls,
    ),  # 처음의 path로 가서 장고가 확인할것이다!
]

# urlpatterns 은 지정된 이름이다
if settings.DEBUG:  # 내가 컴퓨터로 서버돌릴떄만 이렇게 쓴다!
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# static이 경로를 가져다 주는것이다! 컨트롤 클릭해보셈
# URL은 settings.MEDIA_URL이것이고
# 이미지는 settings.MEDIA_ROOT 에서 가져온다!