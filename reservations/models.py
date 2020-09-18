from django.db import models
from core import models as core_models
from django.utils import timezone

# Create your models here.
class Reservation(core_models.TimeStampedModel):
    """ Reservation Model Definition """

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "confirmed"),
        (STATUS_CANCELED, "canceled"),
    )

    status = models.CharField(
        max_length=12, choices=STATUS_CHOICES, default=STATUS_PENDING
    )

    # 유저랑 룸이 삭제되면 예약도 삭제될것이다!!
    check_in = models.DateField()
    check_out = models.DateField()
    guest = models.ForeignKey(
        "users.User", related_name="reservations", on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "rooms.Room", related_name="reservations", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.room} - {self.check_in}"

    # 예약취소 확정같은 예약 상태도 만들수있음, 나중에 추가

    def in_progress(self):
        now = timezone.now().date()
        return now >= self.check_in and now <= self.check_out
        # checkin과 checkout 을 보고 상태 를 결정한다

    in_progress.boolean = True  # X,O 로 상태를 표시해준다!!

    def is_finished(self):
        now = timezone.now().date()
        return now > self.check_out

    is_finished.boolean = True