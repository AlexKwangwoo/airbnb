from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms

# Create your views here.
class LoginView(FormView):
    # 이걸 쓰면 get, post 할필요가없다!

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")
    # reverse는 실제 URL을 준다!
    # reverse_lazy는 바로 실행하지 않는다!
    # 필요할때만 실행한다!
    # 뷰를 불러올때 URL이 아직 불러와지지 않은것이다!
    # 조금 어려운부분이다.. url이 불러 지지않는데 필요할때
    # 바로 가져오게 해주는 lazy를 쓴다고 생각하자!
    # form 에서 제일 좋은점은 우리가 is_valid 같은거 안해도됨!
    # 하나만 하면된다 form_valid!!!

    def form_valid(self, form):  # form이 유효한지만 체크하면 된다!
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)
        # 이게 호출되면 successURL에 다시가고
        # 다시 다 작동된다!


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    initial = {
        "first_name": "Kwang",
        "last_name": "Back",
        "email": "bnc3049@naver.com",
    }
    template_name = "users/signup.html"
    form_class = forms.SignUpForm  # fprms에 정의되어있는 클래스임!
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()  # form이 유효하다면!
        # forms.py에서 만들어진 (form_class = forms.SignUpForm) 형식이 저장된다!
        # 저장하고 다시 로그인해준다!. 회원가입후 사용자가 다시 로그인할필요 없음!
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)

        return super().form_valid(form)


# class LoginView(View):


#     def get(self, request):
#         form = forms.LoginForm(initial={"email": "kwang@g.com"})
#         return render(request, "users/login.html", {"form": form})

#     def post(self, request):
#         form = forms.LoginForm(request.POST)
#         if form.is_valid():

#             # print(form.cleaned_data)
#             # 만약 user/forms에서 아무이상없다면
#             # 정리된 데이터를 전송할것이다!
#             print(form.cleaned_data)
#             email = form.cleaned_data.get("email")
#             password = form.cleaned_data.get("password")
#             user = authenticate(request, username=email, password=password)
#             # authenticate 을 통해 백앤드 프론트앤드 다 연결을 해준다!
#             # 백앤드 로그아웃후,, 프론트에서 로그인해도 백앤드 다시 로그인지속됨!
#             if user is not None:
#                 login(request, user)
#                 return redirect(reverse("core:home"))
#         return render(request, "users/login.html", {"form": form})


# def log_out(request):
#     logout(request)
#     return redirect(reverse("core:home"))