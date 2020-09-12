from django.contrib import admin
from . import models

# . 의 의미는 같은 폴터라는뜻임!

# Register your models here.


@admin.register(models.User)
class CustomUserAdmin(admin.ModelAdmin):
    pass
