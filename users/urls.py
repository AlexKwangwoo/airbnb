from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login", views.LoginView.as_view(), name="login"),
    path("login/github", views.github_login, name="github-login"),
    path("login/github/callback", views.github_callback, name="github-callback"),
    path("logout", views.log_out, name="logout"),
    path("signup", views.SignUpView.as_view(), name="signup"),
    path(
        "verify/<str:key>",
        # 예를들어 http://localhost:8000/users/verify/83bf208087cd4af3a526 에서
        # <str:key>는 83bf208087cd4af3a526를 의미한다! str은 그값이 str 이라는것이다!
        # key(아무이름이나됨)은 view 파일에서 complete_verification의 request 다음 받아온다!
        views.complete_verification,
        name="complete-verification",
    ),
]