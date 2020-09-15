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

    fieldsets = (
        (
            "Basic Info",
            {"fields": ("name", "description", "country", "address", "price")},
        ),
        ("Times", {"fields": ("check_in", "check_out", "instant_book")}),
        ("Spaces", {"fields": ("guests", "beds", "bedrooms", "baths")}),
        (
            "More About the Space",
            {
                "classes": ("collapse",),  # 너무 길면 접는 기능도 추가가능!
                "fields": ("amenities", "facilities", "house_rules"),
            },
        ),
        (
            "Last Details",
            {"fields": ("host",)},  # 한개인 경우 , 가 있어야 튜플이 된다!
        ),
    )

    ordering = ("name", "price", "bedrooms")  # 리스트들을 어떻게 정렬할것인지!!

    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        # aminities 넣고싶은데.. many to many는 안될경우가 있다!!
        # 그럴땐 함수를 만들자!
        "count_photos",
    )

    ###############################################################################
    # 어려부분이다!!!!!!!!!!!!!!!!!!!
    # admin의 함수는 두가지의 arguments 를 가진다
    # 처음은 class RoomAdmin(Room) 여기클래스를 가리키고
    # 두번째 인자는 admin페이지의 리스트 row현재 열을 가진다
    # 즉 자신이 가지고 있는 줄의 amenities의 갯수를 알려줌!
    # obj를 출력해보면
    # 상속받고있기떄문에 models에 있는 room클래스의 __str__을 출력한다
    # 밑의 시설과 밑밑의 사진은 다른 대상을 가리킨다. 시설은 같은 클래스 안에서
    # aminities를 그냥 가져오는것이지만
    # 밑의 포토는 자신클래스의 속성(사진이 없다) 그래서 RoomAdmin(Room)가 뿌려놓은 포린키
    # 를 가지고있는 클래스 photo에서 정보를 받기위해 room_set을 써야했을것이다 하지만
    # related_name ="photo" 를 이용해 정보를 가져올수있는것이다.
    def count_amenities(self, obj):
        return obj.amenities.count()

    # count_amenities.short_description = "hello sexy!"
    # column 제목도 바꿀수있음

    def count_photos(self, obj):
        return obj.photos.count()

    #
    ###############################################################################

    # filter list도 __ 이용하여 host 의 속성 user의 superhostm gender이용가능!!
    list_filter = (
        "instant_book",
        "host__superhost",
        # "host__gender",
        "city",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "country",
    )

    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )  # horizontal filter 은 many to many 이용가능!!

    search_fields = ("^city", "^host__username")
    # search_fields = ("city",) ^ 없으면 bu만 해도 busan찾아진다
    # = 는 정확하게 입력..대소문자!
    # host.username 이 아니라 search는 __ + 속성 값 사용 가능!


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """ Photo Admin Definition"""

    pass