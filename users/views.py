import os
import requests
from django.views import View
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import FormView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile  # 사진보여줄때 필요!
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin  # 프로필 업데이트하면 나오게한다!
from . import forms, models, mixins

# from django.contrib.auth.forms import UserCreationForm # 여기안하고 form에 적용할거임


# Create your views here.
class LoginView(mixins.LoggedOutOnlyView, FormView):
    # 이걸 쓰면 get, post 할필요가없다!

    template_name = "users/login.html"
    form_class = forms.LoginForm
    # success_url = reverse_lazy("core:home") 이거대신 get_success_url을 씀!
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

    def get_success_url(self):
        # LoggedOutOnlyView 가 작동이되면.. airbnb문서 196장에 잘 써놧음!
        # 주소 마지막에 갈려고했던곳..이 next=???로적힌다 그래서 next를 받아오는것이다!
        next_arg = self.request.GET.get("next")
        if next_arg is not None:
            return next_arg
        else:
            return reverse("core:home")


def log_out(request):
    messages.info(request, f"See you later")
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm  # forms에 정의되어있는 클래스임!
    # 비밀번호 (깃허브, 카톡을 위해 form_class를 다른것으로 바꿔준다!)
    # form_class = UserCreationForm
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
        user.verify_email()  # user.model파일에 있는 함수를 사용한다!
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True  # 여기서 확인했다고 알려준다! False=>True
        user.email_secret = ""
        # 메일열고 here 클릭하기전까지는 admin에 secret이 저장되어있음

        user.save()  # 장고 signupview에 자동 저장 기능이있다!
        # to do : add success message
    except models.User.DoesNotExist:
        # to do: add error message
        pass
    return redirect(reverse("core:home"))


# 유저가 깃허브 눌렀을때 /user/login/github링크로갈껀데 redirect 쪽으로 가진다!
def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://localhost:8000/users/login/github/callback"  # 깃허브의 Authorization callback URL
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


# 유저가 accept를 누르면 여기로 온다!! 또한 url에서 code를 가져온다
# http://localhost:8000/users/login/github/callback?code=80bd88bcaafc31e583ee
# 저기서 code=~~~~ 되어있는 부분! 이코드로 우리는 다시 다른 request를 보낼것이다!
# token_access 한다 with client_id, client_secret, code를 이용해서!
# 그다음 깃허브는 우리에게 json을 줄것이고!!(result값으로..)
# 그다음 애러가 있는지 체크 할것이다!
# 에러가 없다면 (else)에서 access_token을 가져올것이다!
# 그 access_token을 가지고 깃허브 api를 request할수있게 된다!
# 헤더에서 토큰을 보내고 그다음 우리는 profile json을 받게된다!
# 그다음 profile json안에 username이 있는지 체크할것이다!
# profile_json 속에 이름이 없다면 리다이렉해준다!


class GithubException(Exception):
    # 이름을 우리껄로 만들었고.. redirect대신 exception을 사용해준다!
    pass


def github_callback(request):
    try:
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        code = request.GET.get("code", None)
        # code를 access token으로 바꿔야한다! 깃허브 api를 access 할수있게 해준다!
        # 우리가 해야하는건 post request를 보내야 한다!
        if code is not None:
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )  # 값을 제이슨으로 넘겨준다고 깃에 쓰어있음!!
            token_json = token_request.json()
            error = token_json.get("error", None)
            # 토큰json에서 에러를 포함한 문서가있는지 봐야한다
            # 예를 들어 유효하지 않은 코드가 왔을때!.. 시간지났던지..등등
            if error is not None:
                # return redirect(reverse("users:login"))
                raise GithubException("Can't get access token")
            else:
                access_token = token_json.get("access_token")
                # 깃허브 API에 request를 보내는걸 만들거임!
                profile_request = requests.get(
                    # 그 access_token을 가지고 깃허브 api를 request할수있게 된다!
                    "https://api.github.com/user",
                    # emails를 써서 프라이빗 메일도 찾아줌! 또는 깃헙 프리베이트 메일해제!
                    # 프리벳 문제생기면 !! 이부분 손봐야함!!
                    # 헤더에서 토큰을 보내고
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                # print(profile_request)
                # 내가만든설명서에 있음 3단계에 적혀있다!! 시키는데로 설명서보고 하는중..
                profile_json = profile_request.json()
                username = profile_json.get("login", None)
                if username is not None:
                    # user가 있다면 계속 진행
                    # 이것들을 깃허브에서 가져온다!!
                    name = profile_json.get("name")
                    email = profile_json.get("email")
                    bio = profile_json.get("bio")

                    # 그 이메일을 가진 유저가 있다면 그말은 이미 로그인 되어 있다는 뜻이다.
                    # 그 이메일을 가진 user가 있다는 뜻이다
                    try:
                        user = models.User.objects.get(email=email)
                        # 만약 우리가 유저를 찾았다면 로그인 메소드를 확인할것이다
                        if user.login_method != models.User.LOGIN_GITHUB:
                            # trying to log in 여기 온다는건 밑에 모든 조건을 다 거쳤다는것이다!
                            # 만약 로그인메쏘드가 깃허브면 유저를 로그인 시킬것이다!
                            # login(request, user) 밑에서 한번에 해줌
                            raise GithubException(
                                f"Please log in with: {user.login_method}"
                            )

                    except models.User.DoesNotExist:
                        # 만약 우리가 한명의 유저도 찾을 수 없다면.. 그뜻은
                        # 우리가 유저를 만들어야한다는 의미 이다!
                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                            # 이유저는 깃허브로 부터 왔다!
                        )
                        user.set_unusable_password()
                        # 어떤 패스워드가 됐던 먹히지 않고
                        # 로그인 시킬것이다!
                        user.save()
                    login(request, user)
                    messages.success(request, f"Welcome back {user.first_name}")
                    return redirect(reverse("core:home"))

                else:
                    # return redirect(
                    #     reverse("users:login")
                    # )  # profile_json 속에 이름이 없다면 리다이렉해준다!
                    raise GithubException("Can't get your profile")
        else:
            # return redirect(reverse("core:home"))
            # 코드가 none이면
            raise GithubException("Can't get code")
    except GithubException as err:  # 에러나면 걍 로그인으로 보냄
        messages.error(request, err)
        return redirect(reverse("users:login"))


def kakao_login(request):
    client_id = os.environ.get("KAKAO_ID")
    redirect_uri = "http://localhost:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO_ID")
        redirect_uri = "http://localhost:8000/users/login/kakao/callback"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )  # 여기서 access token을 얻는다!
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException("Can't get authorization code")
        access_token = token_json.get("access_token")
        # if 검사후 json에 access token이 있다.. get으로 가져온다!
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",  # 와... 한칸 띄워져 있었다고 404오류 계쏙남... me다음에
            headers={"Authorization": f"Bearer {access_token}"},
        )  # 카카오톡 문서에 나와있다!

        profile_json = profile_request.json()
        email = profile_json.get("kakao_account").get("email")
        # 여기서 kaccount_email은 json의 속성이름으로 바꾸면 안된다!
        if email is None:
            raise KakaoException("Please also give us your email")
        properties = profile_json.get("properties")
        nickname = properties.get("nickname", None)
        profile_image = (
            profile_json.get("kakao_account", None)
            .get("profile", None)
            .get("profile_image_url", None)
        )
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException(f"Please log in in with: {user.login_method}")
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True,
                # 이유저는 카카오로 부터 왔다!
            )
            user.set_unusable_password()
            user.save()
            if profile_image is not None:  # 사진을 넣고싶으면 이렇게 하자!! 외우자!!
                # import 만 잘해주면된다!!
                photo_request = requests.get(profile_image)  # URL로 부터 request한다!
                # photo_request.content()  # 0,1 바이트다! 그게 content다!
                user.avatar.save(
                    f"{nickname}-avatar.jpg", ContentFile(photo_request.content)
                )  # ContentFile 안해주면.. 엄청 긴 글자만 보인다!, 그리고 저장된다!
        messages.success(request, f"Welcome back {user.first_name}")
        login(request, user)
        return redirect(reverse("core:home"))
    except KakaoException as err:
        messages.error(request, err)
        return redirect(reverse("users:login"))


class UserProfileView(DetailView):
    model = models.User
    context_object_name = "user_obj"


class UpdateProfileView(mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    model = models.User
    template_name = "users/update-profile.html"
    fields = (
        "first_name",
        "last_name",
        "gender",
        "bio",
        "birthdate",
        "language",
        "currency",
    )  # model form처럼 하고있다!

    success_message = "Profile Updated"  # 프로필 업데이트하면 나오게한다!

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["first_name"].widget.attrs = {"placeholder": "First name"}
        form.fields["last_name"].widget.attrs = {"placeholder": "Last name"}
        form.fields["bio"].widget.attrs = {"placeholder": "Bio"}
        form.fields["birthdate"].widget.attrs = {"placeholder": "Birthdate"}
        return form  # 이것을 통해서 updateview에서도 플래이스홀더 사용할수있음!


class UpdatePasswordView(
    mixins.EmailLoginOnlyView,
    mixins.LoggedInOnlyView,
    SuccessMessageMixin,
    PasswordChangeView,
):
    template_name = "users/update-password.html"
    success_message = "Password Updated"

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields["old_password"].widget.attrs = {"placeholder": "Current password"}
        form.fields["new_password1"].widget.attrs = {"placeholder": "New password"}
        form.fields["new_password2"].widget.attrs = {
            "placeholder": "Confirm new password"
        }
        return form  # 이것을 통해서 updateview에서도 플래이스홀더 사용할수있음!

    def get_success_url(self):
        return self.request.user.get_absolute_url()


# @login_required
# def start_hosting(request):
#     request.session["is_hosting"] = True
#     return redirect(reverse("core:home"))
#     # 호스트가 된사람만이 방을 만들수있게 해줄려는 작업이다!


@login_required
def switch_hosting(request):
    # 이함수가 콜되면 처음 del한다.. 만약 호스트접속이면..
    # 이함수가 콜되면 keyError 가 뜨면 호스트가 되게끔 True로 바꿔준다!
    try:
        del request.session["is_hosting"]
    except KeyError:  #
        request.session["is_hosting"] = True
    return redirect(reverse("core:home"))

    # def form_valid(self, form):
    #     email = form.cleaned_data.get("email")
    #     self.object.username = email
    #     self.object.save()
    #     return super().form_valid(form)
    #  form_valid를 통해 정보를 가로채서 저장을 다른곳에 해준다.!
    # 예를들어 이메일로받고 그 이메일은 id에 저장을 해버린다!

    # 이렇게 해줌으로써 프로파일 내꺼 누르고 다른사람누르고..다시내껄 누를때
    # 남게 아닌 내껄 볼수있다!! user_detail도  {{user.first_name}} 이 아니라
    # {{user_obj.first_name}}로 수정했음!

    # 뭔가 좀더 text를 넣고 싶을때
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # 언제나 get_context_data sms 위의 user_obj를 주기때문에 다른것도 바뀐다
    #     # 그래서 새로운거 할려면 super를 써야한다!
    #     context["Hello"] = "Hello!"
    #     return context


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