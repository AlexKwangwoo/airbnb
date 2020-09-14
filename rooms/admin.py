from django.contrib import admin
from . import models

# Register your models here.


@admin.register(
    models.RoomType, models.Facility, models.Amenity, models.HouseRule
)  # RoomType 등등 을 admin패널에 넣겠습니다!
class ItemAdmin(admin.ModelAdmin):
    """ Item Admin Definition """

    pass


# 장고의 contrib에서 admin 파일에 Room이라는 클래스를 가져오는것임!
@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    """ Room Admin Definition """

    pass


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """ Photo Admin Definition"""

    pass