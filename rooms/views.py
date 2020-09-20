from django.views.generic import ListView, DetailView, View
from django.shortcuts import render
from django_countries import countries
from django.core.paginator import Paginator
from . import models, forms

# from django.http import Http404
# from django.shortcuts import render
# from math import ceil
# from django.shortcuts import render, redirect
# from django.urls import reverse
# from django.utils import timezone
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
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     now = timezone.now()
    #     context["now"] = now
    #     return context


# view를 더 쉽게 해보자!! 장고가 많이 도와주는 세번째 방식으로!
class RoomDetail(DetailView):
    """ RoomDetail Definition """

    model = models.Room  # 장고가 models.Room의 Room을 소문자로 바꿔
    # room detail.html 의 room 변수로 사용하게 만들어준다!!
    # view한테 우리가 무슨 model을 원하는지 알려줘야한다!


class SearchView(View):
    """ SearchView Definition """

    def get(self, request):
        country = request.GET.get("country")
        if country:

            form = forms.SearchForm(request.GET)

            if form.is_valid():  # 애러가 없으면 리턴 true, 있으면 false
                # 여기 모든 왼쪽 값들은 룸 모델에서 가져온것이다!!
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")
                house_rules = form.cleaned_data.get("house_rules")

                # 장고가 알아서 파일 타입을 알고있기에 대입해준다!.
                # 장고 form안쓸때는 일일히 우리가 int str 등 타입에 맞게 해줬어야했다!!
                filter_args = {}
                # filter_args에 들어올때마다 if-> if-> if-> 탄다고 보면됨
                # 점점 걸러준다!

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type
                    # room_type.pk == room_type 이라고 보면된다!!
                    # 장고가 뛰어나서 알아서 해줌.. 걍 pk지워야함!

                if price is not None:
                    filter_args["price__lte"] = price
                    # lte => less than equals// price보다 낮은 가격을 찾아준다!

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                # print(bool(instant), bool(superhost))

                if instant_book is True:
                    filter_args["instant_book"] = True
                    # instant_book 이 True면 포함시켜주세요!

                if superhost is True:
                    filter_args["host__superhost"] = True

                    # if len(s_amenities) > 0:
                    # array 때문에 걸러줘야한다!!
                    # s_amenities에서 [1,2,3]을 가지고있다면 1,2,3을 필터에 하나하나 추가하는것!!
                for amenity in amenities:
                    filter_args["amenities"] = amenity  # __pk없어도된다!!!!!

                    # if len(s_facilities) > 0:  # array 때문에 걸러줘야한다!! 장고가 알아서 다처리해준다!
                for facility in facilities:
                    filter_args["facilities"] = facility

                    # if len(s_house_rules) > 0:  # array 때문에 걸러줘야한다!!
                for house_rule in house_rules:
                    filter_args["house_rules"] = house_rule
                # city + __startswith 에 의해 입력된 값으로 시작된 단어를 찾아준다! city에서!
                # 그래서 seo 입력경우 시티가 seoul인 경우 rooms에 들어가게된다!!
                # country 는 선택값이 정해져있기때문에 조건 없고 시작 글자도 필요없다!

                qs = models.Room.objects.filter(**filter_args).order_by("-created")

                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)
                return render(
                    request,
                    "rooms/search.html",
                    {"form": form, "rooms": rooms},  # form = forms.searchForm 에서 가져옴!
                )

        else:
            form = forms.SearchForm()
            # 종종 데이터 확인 작업없이 빈 form필요할때 있음, ex)처음 form화면!
            # request.GET을 해주면.. form에서 입력한게
            # 자동으로 서치 눌러도 같은 값을 가지고 있다!!
        return render(
            request,
            "rooms/search.html",
            {"form": form},  # form = forms.searchForm 에서 가져옴!
        )

    # city = request.GET.get("city", "Anywhere")
    # city = str.capitalize(city)
    # country = request.GET.get("country", "KR")
    # room_type = int(request.GET.get("room_type", 0))
    # price = int(request.GET.get("price", 0))
    # guests = int(request.GET.get("guests", 0))
    # bedrooms = int(request.GET.get("bedrooms", 0))
    # beds = int(request.GET.get("beds", 0))
    # baths = int(request.GET.get("baths", 0))
    # instant = bool(request.GET.get("instant", False))
    # superhost = bool(request.GET.get("superhost", False))  # 필터를 위해 bool값으로 바꿔준다!
    # s_amenities = request.GET.getlist("amenities")
    # s_facilities = request.GET.getlist("facilities")
    # s_house_rules = request.GET.getlist("house_rules")
    # # getlist를 통해 amenity와 facility의 checkbox에서 선택된
    # # 친구들의 리스트를 가져올수 있게 된다!!

    # form = {
    #     "city": city,
    #     "s_room_type": room_type,
    #     "s_country": country,
    #     "price": price,
    #     "guests": guests,
    #     "bedrooms": bedrooms,
    #     "beds": beds,
    #     "baths": baths,
    #     "s_amenities": s_amenities,
    #     "s_facilities": s_facilities,
    #     "s_house_rules": s_house_rules,
    #     "instant": instant,
    #     "superhost": superhost,
    # }  # request로 오는 정보는 다 form으로 갈것이다! 즉 get으로 받는정보는 여기서!! 표시해줌!

    # room_types = models.RoomType.objects.all()
    # amenities = models.Amenity.objects.all()
    # facilities = models.Facility.objects.all()
    # house_rules = models.HouseRule.objects.all()

    # choices = {
    #     "countries": countries,
    #     "room_types": room_types,
    #     "amenities": amenities,
    #     "facilities": facilities,
    #     "house_rules": house_rules,
    # }

    # filter_args = {}
    # # filter_args에 들어올때마다 if-> if-> if-> 탄다고 보면됨
    # # 점점 걸러준다!

    # if city != "Anywhere":
    #     filter_args["city__startswith"] = city

    # filter_args["country"] = country

    # if room_type != 0:
    #     filter_args["room_type__pk__exact"] = room_type
    #     # room_type.pk == room_type 이라고 보면된다!!

    # if price != 0:
    #     filter_args["price__lte"] = price
    #     # lte => less than equals// price보다 낮은 가격을 찾아준다!

    # if guests != 0:
    #     filter_args["guests__gte"] = guests

    # if bedrooms != 0:
    #     filter_args["bedrooms__gte"] = bedrooms

    # if beds != 0:
    #     filter_args["beds__gte"] = beds

    # if baths != 0:
    #     filter_args["baths__gte"] = baths

    # # print(bool(instant), bool(superhost))

    # if instant is True:
    #     filter_args["instant_book"] = True
    #     # instant_book 이 True면 포함시켜주세요!

    # if superhost is True:
    #     filter_args["host__superhost"] = True

    # if len(s_amenities) > 0:
    #     # array 때문에 걸러줘야한다!!
    #     # s_amenities에서 [1,2,3]을 가지고있다면 1,2,3을 필터에 하나하나 추가하는것!!
    #     for s_amenity in s_amenities:
    #         filter_args["amenities__pk"] = int(s_amenity)

    # if len(s_facilities) > 0:  # array 때문에 걸러줘야한다!!
    #     for s_facility in s_facilities:
    #         filter_args["facilities__pk"] = int(s_facility)

    # if len(s_house_rules) > 0:  # array 때문에 걸러줘야한다!!
    #     for s_house_rule in s_house_rules:
    #         filter_args["house_rules__pk"] = int(s_house_rule)

    # rooms = models.Room.objects.filter(**filter_args)
    # # city + __startswith 에 의해 입력된 값으로 시작된 단어를 찾아준다! city에서!
    # # 그래서 seo 입력경우 시티가 seoul인 경우 rooms에 들어가게된다!!
    # # country 는 선택값이 정해져있기때문에 조건 없고 시작 글자도 필요없다!
    # return render(
    #     request,
    #     "rooms/search.html",
    #     {**form, **choices, "rooms": rooms},
    #     # {form, choices}이것은 뭉쳐있기때문에 **를 써서 풀어준다(dictionary)
    # )


# url에서 pk를 가지고 올것이다!!
# 이제 데이터베이스에서 room 정보를 가지고 온다!
# render request받고 rooms에 있는 탬플릿 detail을 실행시킨다!
# def room_detail(request, pk):
#     try:
#         room = models.Room.objects.get(pk=pk)
#         return render(request, "rooms/detail.html", {"room": room})
#     except models.Room.DoesNotExist:
#         raise Http404()
# 장고는 탬플릿폴더!!! 바로!!안의404.html을 자동으로 찾아간다!!
# 템플릿 속 다른 파일안에 있으면 안된다!
# 에러 뜨게 하고싶으면 return이 아니라 raise이다!!
# return redirect(reverse("core:home"))
# reverse를 통해 주소 설정이 쉬움!!

# render의 마지막은 탬플릿에서 사용할 변수가 될것이다! ex)room.name
# "room":room에서 두번째 room은 위에 models.Room.~~ 이다!


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
