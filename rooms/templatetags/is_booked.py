import datetime
from django import template
from reservations import models as reservation_models

register = template.Library()

# simple_tag가 context를 받을 수 있게 하면 우리는 user의 정보를 가지고
# 뭔가를 하거나 할수있음! register.simple_tag(takes_context=True)
# sext_capitals의 필터보다 tag가 더 좋다.. 이유는 tag에 더많은 인자 전달 가능!
@register.simple_tag
def is_booked(room, day):
    if day.number == 0:
        return
        # 만약 0이면.. 즉 0 0 0 0 1 2 3 이런식으로 날짜가 시작되면.. 0은 아무것도 리턴안함
    try:
        # 그날짜가 0이 아니면.. date객체를 만들어 줄것이다!
        # 왜냐하면 bookedday는 datetime형식을 가지는 object이라서!
        date = datetime.datetime(year=day.year, month=day.month, day=day.number)
        # 그다음.. bookedday가 있는지 없는지 체크하는데 조건은 day는 위의 date이고!
        # 그다음 조건에는 relation을 이용해서 reservation의 room을 가지고 와서 __room=room해줌!
        # =room 의 room은 템플릿에서 받은거!
        reservation_models.BookedDay.objects.get(day=date, reservation__room=room)
        # 만약에 우리가 bookedDay를 찾았으면 True를 리턴하고!
        return True
    except reservation_models.BookedDay.DoesNotExist:
        return False
