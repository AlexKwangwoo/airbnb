from django.contrib import admin
from django.utils.html import mark_safe  # 장고 security 해제
from . import models


# Register your models here.


@admin.register(
    models.RoomType, models.Facility, models.Amenity, models.HouseRule
)  # RoomType 등등 을 admin패널에 넣겠습니다!
class ItemAdmin(admin.ModelAdmin):
    """ Item Admin Definition """

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()
        # room에 의해 몇번 쓰였는지!
        # 여기서 rooms는 클래스 Rooms의 related_name 을 가리킨다!!


# admin 속에 다른 admin넣는 방법!!
class PhotoInlines(admin.TabularInline):
    model = models.Photo  # 어떤 클래스의 모델을 넣겠습니까? photo!


# 장고의 contrib에서 admin 파일에 Room이라는 클래스를 가져오는것임!
@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    """ Room Admin Definition """

    inlines = (PhotoInlines,)  # 위에 photoInline을 추가해주면 된다!

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "name",
                    "description",
                    "country",
                    "city",
                    "address",
                    "price",
                    "room_type",
                )
            },
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

    # list_display가 처음 룸눌렀을때 보이는것.. 개인적인 방
    # 자체를 누르면 fieldset이 실행된다!

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
        "total_rating",
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
        # obj는 위의 RoomAdmin 클래스가리킴->상속 room받고있음
        # photo를 한 related name을 찾는다!!
        # Photo클래스의 related_name ="photo" 이다!

    count_photos.short_description = "Photo Count"

    #
    ###############################################################################

    # 이부분은 admin의 저장을 컨트롤할수있다!
    # def save_model(self, request, obj, form, change):
    #     print(obj, change, form)
    #     super().save_model(request, obj, form, change)  # Call the real save() method

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

    raw_id_fields = ("host",)
    # userAdmin을 사용해서  유저를 검색할수있게 해준다!!!!!!

    filter_horizontal = (
        "amenities",
        "facilities",
        "house_rules",
    )  # horizontal filter 은 many to many 이용가능!!

    search_fields = ("^city", "^host__username", "name")
    # 여기서 admin에서 방 검색 할때 뭘로 찾아줄지 추가할수있다!
    # search_fields = ("city",) ^ 없으면 bu만 해도 busan찾아진다
    # = 는 정확하게 입력..대소문자!
    # host.username 이 아니라 search는 __ + 속성 값 사용 가능!


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """ Photo Admin Definition"""

    list_display = ("__str__", "get_thumbnail")

    # 이것은 프론트 앤드에서 안쓰기에 모델에 넣을필요없다
    def get_thumbnail(self, obj):
        return mark_safe(f'<img width = 50px, src="{obj.file.url}" />')

    # mark_safe 안써주면.. 장고의 security 가 작동해 경로를 변경한다!
    # import 후 사용해주자!
    get_thumbnail.short_description = "Thumbnail"