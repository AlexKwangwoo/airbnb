from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# . 의 의미는 같은 폴터라는뜻임!

# Register your models here.

# admin.site.register(models.User, CustomUserAdmin) 이랑 똑같음
# admin 패널에서 user를 보고싶음!!
# 바로 밑에 있어야함!!
# 장고의 contrib에서 admin 파일에 User이라는 클래스를 가져오는것임!
@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    """ Custom User Admin """

    # 처음에는 UserAdmin이아니라 admin.ModelAdmin이 였음. 모든게 사용자가 설정
    # UserAdmin은 월래 있던 기존의 장고의 패널을 사용하겠다는 뜻
    # list_display = "username", "email", "gender", "language", "currency", "superhost"
    # admin 페이지에서 list 들을 보여준다!
    # list_filter = ("language", "superhost", "currency")
    # 위와 같이 해서 유저 마음대로의 패널을 제작했었음

    # 여기서부터는 UserAdmin을 사용하여 UserAdmin과 사용자가 만든 패널을 같이보여줌
    # fieldsets 는 장고에서 지정된 변수임.. 바꾸면 안됨!
    # userAdmin을 컨트롤 클릭해보면 클래스 지정변수인걸 알수있음!
    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "superhost",  # 여기서 만들어지는 모든것들의 이름 첫글자는 자동으로 대문자가 된다
                )
            },
        ),
    )

    list_filter = UserAdmin.list_filter + ("superhost",)

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
        "email_verified",
        "email_secret",
    )
    # is_ ~~~ 친구들은 클래스 User가 상속받은
    # AbstractUser 속에 있는 정해진 값이다!!!
    # 그대로 써야함!
