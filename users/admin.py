from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# . 의 의미는 같은 폴터라는뜻임!

# Register your models here.

# admin.site.register(models.User, CustomUserAdmin) 이랑 똑같음
# admin 패널에서 user를 보고싶음!!
# 바로 밑에 있어야함!!
@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    """ Custom User Admin """

    # list_display = ("username", "email", "gender", "language", "currency", "superhost")
    # admin 페이지에서 list 들을 보여준다!
    # list_filter = ("language", "superhost", "currency")

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
                    "superhost",
                )
            },
        ),
    )
