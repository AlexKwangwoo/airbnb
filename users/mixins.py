from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect, reverse


class EmailLoginOnlyView(UserPassesTestMixin):
    # 누군가 이메일 이용해서.. 즉 카카오 깃허브로 접속해서는
    # 비밀번호 바꾸는 창으로 갈수가 없다
    def test_func(self):
        return self.request.user.login_method == "email"

    def handle_no_permission(self):
        messages.error(self.request, _("Can't go there"))  # 애러 번역!
        return redirect("core:home")


class LoggedOutOnlyView(UserPassesTestMixin):

    permission_denied_message = "Page not found"

    def test_func(self):
        return not self.request.user.is_authenticated
        # 함수는 true만 반환하는데... not을 붙임으로써 false를 줘야 true가 된다!
        # 즉 권한이 부여되지 않은 유저는 결과값이 true로 되어 다음 함수로 넘어간다!
        # true 값은 유저는 인증이 되지 않았다는것을 의미..즉 익명의 유저
        # 즉.. 로그인 안된사람이.. /login 때 걍 패스를 해주지.. 로그인된사람이
        # /login하면.. 밑의 함수가 실행된다! 즉 로그인 된사람만
        # handle no permission이 발생된다 메인홈페이지로 돌아감!

    def handle_no_permission(self):
        messages.error(self.request, "Can't go there !!")
        return redirect("core:home")


class LoggedInOnlyView(LoginRequiredMixin):  # LoginRequiredMixin test_func을 기본적으로 가짐
    # 유저가 인증안되면 유저를 로그인되게 해줄거임
    login_url = reverse_lazy("users:login")
