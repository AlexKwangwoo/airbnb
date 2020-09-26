import datetime
from django.http import Http404
from django.views.generic import View
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from rooms import models as room_models
from reviews import forms as review_forms
from . import models


class CreateError(Exception):
    pass


# Create your views here.


def create(request, room, year, month, day):
    try:
        date_obj = datetime.datetime(year, month, day)
        room = room_models.Room.objects.get(pk=room)
        models.BookedDay.objects.get(day=date_obj, reservation__room=room)
        # booked day가있으면 다른 예약이 있다니깐 에러를 이르킨다!
        raise CreateError()
    except (room_models.Room.DoesNotExist, CreateError):
        # 룸을 못찾을 때 나온다!
        messages.error(request, "Can't Reserve That Room")
        return redirect(reverse("core:home"))
    except models.BookedDay.DoesNotExist:
        # 예약된게 없다면!!!
        reservation = models.Reservation.objects.create(
            guest=request.user,
            room=room,
            check_in=date_obj,
            check_out=date_obj + datetime.timedelta(days=1),
            # check_out은 하루 다음날.. 장고는 2일연속 못한다!
        )
        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


class ReservationDetailView(View):
    # view를 쓰는이유는 컨트롤 하기 위해서! detail쓸수도 있으나..
    # detail보다 좀더 복잡하게 만들고 싶다
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        # reservation = models.Reservation.objects.get(pk=pk)
        # get은 결과를 찾지 못하면 error를 발생시킨다!.. DoesNotExist말고 다르게 해보자
        reservation = models.Reservation.objects.get_or_none(pk=pk)
        # 여기 pk=pk 인자 값들은.. CustomReservationManager의 get or none의
        # **kwargs 의 쿼리 인자로 받을수있따!
        # managers 에 정의하고 model에 추가해서 쓸수있다!
        # 이 reservation은 guest나 host한테만 보여질 것이다!
        if not reservation or (
            reservation.guest != self.request.user
            and reservation.room.host != self.request.user
        ):
            raise Http404()
        # 페이지를 요청하는 user는 guest나 host여야 한다!
        # 즉 호스트도 게스트도 아니라면 http404를 raise한다!
        form = review_forms.CreateReviewForm()  # review의 폼을 받아와서 밑에 보내준다
        return render(
            self.request,
            "reservations/detail.html",
            {"reservation": reservation, "form": form},
        )


def edit_reservation(request, pk, verb):
    reservation = models.Reservation.objects.get_or_none(pk=pk)
    # 여기 pk=pk 인자 값들은.. CustomReservationManager의 get or none의
    # **kwargs 의 쿼리 인자로 받을수있따!
    # managers 에 정의하고 model에 추가해서 쓸수있다!
    # 이 reservation은 guest나 host한테만 보여질 것이다!
    if not reservation or (
        reservation.guest != request.user and reservation.room.host != request.user
    ):
        raise Http404()
        # 페이지를 요청하는 user는 guest나 host여야 한다!
        # 즉 호스트도 게스트도 아니라면 http404를 raise한다!
    if verb == "confirm":
        reservation.status = models.Reservation.STATUS_CONFIRMED
    elif verb == "cancel":
        reservation.status = models.Reservation.STATUS_CANCELED
        print(models.BookedDay.objects.filter(reservation=reservation))
        models.BookedDay.objects.filter(reservation=reservation).delete()
    reservation.save()
    messages.success(request, "Reservation Updated")
    return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))
