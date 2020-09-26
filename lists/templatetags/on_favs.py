from django import template
from lists import models as list_models

register = template.Library()


@register.simple_tag(takes_context=True)
def on_favs(context, room):
    user = context.request.user
    the_list = list_models.List.objects.get_or_none(
        user=user, name="My Favourites Houses"
    )
    # room in the_list.rooms.all()
    # 얘는 템플릿태그를 call할것이다 장고의 context object로!
    # 이제 우리는 room_detail을 이용할수있다!
    # print(context, room)
    # print(context.request.user) 유저 확인!
    if the_list:
        return room in the_list.rooms.all()
    else:
        return False
    # 리스트를 불러오는데.. 유저가 내가 request한 유저랑 같은 목록만 불러온다!
    # 리스트가 두개면.. 에러를 일으킬 것이다!
    # 만약 룸이 리스트안에 있다면!!
    # room in the_list.rooms.all()
