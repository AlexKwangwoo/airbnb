from django.utils import timezone
from django.views.generic import ListView
from . import models

# from math import ceil
# from django.shortcuts import render, redirect
# from django.core.paginator import Paginator, EmptyPage
# from datetime import datetime
# from django.http import HttpResponse

# Create your views here.
# 클래스를 만들어주면서 탬플릿 rooms에 room_list를 만들어줌
# 이름 바뀌면 안됨! 컴파일러가 원함! import, render 할필요가없다!!
class HomeView(ListView):
    """ HomeView Definition """

    model = models.Room
    paginate_by = 10
    # 정해져 있는 변수다.. 10줄기준으로 나눔.. 한줄로 끝!!!
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"

    # context 안의 내용을 좀더 수정한다!!!! 시간 추가!
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
        return context


# 밑에꺼는 get_page사용이고 지금은 에러발생시키는 page 를 보자!
# def all_rooms(request):
#     page = request.GET.get("page", 1)
#     room_list = models.Room.objects.all()
#     paginator = Paginator(room_list, 10, orphans=5)
#     try:
#         rooms = paginator.page(int(page))  # <-!!!! 이부분이getpage랑 다르다
#         return render(request, "rooms/home.html", {"page": rooms})
#         # 페이지 범위를 넘어가면 오류가 난다!
#     except EmptyPage:
#         # rooms = paginator.page(1)  # 예외뜨면 페이지 1로 이동해라!
#         # 사용자가 (/?page=12312412) url이 지저분해지는 redirection 하자!
#         return redirect("/")


# # 장고의 도움을 가지고 만들어 보자!(get_page)는 대부분의 애러를 자동으로
# # 처리해준다!!ex) 31231페이지도 마지막페이지로 보냄
# def all_rooms(request):
#     page = request.GET.get("page")
#     room_list = models.Room.objects.all()
#     # 여기 까진 데이터가 room_list에 로드된게 아니다 room_list를 어디에 써야 호출됨!
#     paginator = Paginator(room_list, 10, orphans=5)
#     # ->[0:10]과 같은 역할을 해준다!
#     # 추가로 orpahns 는 마지막페이지에 적은 갯수가 보여지기 싫을때 마지막페이지 -1
#     # 페이지에 마지막 페이지있던 떨이들을 다 같이 마지막 전 페이지에서 보여준다!
#     rooms = paginator.get_page(page)
#     return render(request, "rooms/home.html", {"page": rooms})


# 여기까진 장고의 별도움없이 만든것!!!
# def all_rooms(request):  # request가 없으면 응답할수없다!
#     page = request.GET.get("page", 1)  # 페이지없으면 1을 준다!
#     page = int(page or 1)  # int안의 page 값이 없으면 1을준다!
#     page_size = 10
#     limit = page_size * page
#     offset = limit - page_size
#     all_rooms = models.Room.objects.all()[offset:limit]
#     # now1 = datetime.now()  # now,hungry는 변수고 탬플릿으로 전송가능
#     # hungry1 = True  # context를이용해서!! 보낼수있음
#     # return HttpResponse(content=f"<h1>{now}</h1>")
#     # request가 오면 hello로 답한다 html형식으로 전달가능!
#     # return render(request, "all_rooms.html", context={"now": now1, "hungry": hungry1})
#     # reponse 없는 request는 없다 그리고 template 이름이 필요!
#     # 우리는 매번 HttpResponse로 답을 못해줌.. 그래서 템플릿을
#     # 사용할것임 템플릿은 html인데 파이썬이 컴파일해줄것임!

#     page_count = ceil(models.Room.objects.count() / page_size)
#     return render(
#         request,
#         "rooms/home.html",
#         context={
#             "rooms": all_rooms,
#             "page": page,
#             "page_count": page_count,
#             "page_range": range(1, page_count),
#         },
#     )
