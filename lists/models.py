from django.db import models
from core import models as core_models


# Create your models here.


class List(core_models.TimeStampedModel):
    """ List Model Definition """

    name = models.CharField(max_length=80)

    # 유저가 지워지면 리스트도 삭제됨
    user = models.OneToOneField(
        "users.User", related_name="list", on_delete=models.CASCADE
    )

    # 리스트는 많은 방들을 가질 수 있다
    rooms = models.ManyToManyField("rooms.Room", blank=True)

    def __str__(self):
        return self.name

    def count_rooms(self):
        return self.rooms.count()  # 바로 변수 rooms를 나타낸다

    count_rooms.short_description = "Number of Rooms"
