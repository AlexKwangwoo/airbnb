import datetime
from django.db import models
from core import models as core_models
from django.utils import timezone

# from . import managers


class BookedDay(core_models.TimeStampedModel):
    day = models.DateField()
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Booked Day"
        verbose_name_plural = "Booked Days"

    def __str__(self):
        return str(self.day)  # str안하면.. 문자가 아니기떄문에 지울때 영향이갔음!


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
    # objects = managers.CustomReservationManager()

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
        is_finished = now > self.check_out
        if is_finished:
            BookedDay.objects.filter(reservation=self).delete()
        return is_finished  # 예약날짜가 끝날때마다 지워준다!

    is_finished.boolean = True

    def save(self, *args, **kwargs):
        print(self, "이게 쏄프")
        if self.pk is None:
            # 예약이 있는지 없는지 체크한다! None이면 우리가 생성하려는
            # 모델이 새로운 거라는 뜻이고
            # 그다음 우리는 start와 end date를 얻을 것이다!
            start = self.check_in
            end = self.check_out
            difference = end - start
            print(self.pk)
            print("reservation pk가 없다고 나옴!")
            existing_booked_day = BookedDay.objects.filter(
                day__range=(start, end)
            ).exists()
            # 그래서 필터를 통해 start와 end사이에 bookedDay가 있는지 확인한다!
            # 존재한다면 existing_booked_day에 값이 들어갈것이다!
            if not existing_booked_day:
                # 존재하지 않는다면.. 우리는 reservation을 저장할거다
                super().save(*args, **kwargs)
                # 여기서 save 해주는 이유는 save를 해야 밑에 reseravtion의 FK를 줄수있음!
                for i in range(difference.days + 1):
                    # i는 0부터  range가 0부터시작한다!
                    day = start + datetime.timedelta(days=i)
                    # 새로운 날짜를 만들어 준다!
                    BookedDay.objects.create(day=day, reservation=self)
                    # 그리고 start와 end사이의 날짜들의 obejct bookedDay를 만들어 준다!
                    # class BookedDay(core_models.TimeStampedModel):
                    # day = models.DateField()
                    # reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE)
                    # 여기 day값과 reservation 값을 넣어준것이다!
                    # reservation 가 포린키가 되는것이다!
                return
        return super().save(*args, **kwargs)