from django.db import models
from core import models as core_models

# Create your models here.
class Review(core_models.TimeStampedModel):
    """ Review Model Definition """

    review = models.TextField()
    accuracy = models.IntegerField()
    communication = models.IntegerField()
    cleanliness = models.IntegerField()
    location = models.IntegerField()
    check_in = models.IntegerField()
    value = models.IntegerField()
    user = models.ForeignKey(
        "users.User", related_name="reviews", on_delete=models.CASCADE
    )
    # 유저가 지워지면 리뷰도 지워진다
    room = models.ForeignKey(
        "rooms.Room", related_name="reviews", on_delete=models.CASCADE
    )
    # 룸이 지워지면 리뷰도 지워진다!! , " " 안에 룸 안넣어주면 import 해야함

    def __str__(self):
        return f"{self.review} - {self.room}"
        # 위의 room은 -> rooms의 Room클래스와 연결 되어있다
        # Room 클래스의 모든 속성의 값을 가져 올 수 있다
