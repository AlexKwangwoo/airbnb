from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView
from rooms import models as room_models
from . import models

# Create your views here.
def toggle_room(request, room_pk):
    action = request.GET.get("action", None)
    # room_pk -> 룸의 pk라는 뜻임!
    # 먼저 리스트를 가져와야한다!
    # room과 pk를 추가해야한다!
    room = room_models.Room.objects.get_or_none(pk=room_pk)  # as room_models를 쓴거임!
    if room is not None and action is not None:
        the_list, _ = models.List.objects.get_or_create(
            user=request.user, name="My Favourites Houses"
        )  # get_or_create와 같은 get은 하나의 객체만 찾아옴.. 만약
        # 두개 이상이면 오류를 일으킬 것임!
        # 튜플을 가진 리스트라.. 내용 하나가 더 올수있으니
        #  _ 를 통해 상관없다 unpack 해주자
        # the_list부분 엄청 중요하다!
        if action == "add":
            the_list.rooms.add(room)  # many to many에 추가 / save를 call할 필요는 없음!
        elif action == "remove":
            the_list.rooms.remove(room)
    return redirect(reverse("rooms:detail", kwargs={"pk": room_pk}))


class SeeFavsView(TemplateView):
    template_name = "lists/list_detail.html"
