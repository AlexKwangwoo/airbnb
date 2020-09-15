from django.db import models
from core import models as core_models


# Create your models here.


class List(core_models.TimeStampedModel):
    """ List Model Definition """

    name = models.CharField(max_length=80)

    # 유저가 지워지면 리스트도 삭제됨
    user = models.ForeignKey(
        "users.User", related_name="lists", on_delete=models.CASCADE
    )

    # 리스트는 많은 방들을 가질 수 있다
    rooms = models.ManyToManyField("rooms.Room", blank=True)

    def __str__(self):
        return self.name
