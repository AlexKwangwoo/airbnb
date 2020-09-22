import uuid  # 번호 무작위 생성!! 8진수 가능(메일검증위해!)
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.shortcuts import reverse
from django.template.loader import render_to_string  # 탬플릿을 load해서 render 한다!

# 유저파트는 위에것을 import 해서 사용할것이다..


# Create your models here.
# 장고 속의 models속의 class Model을 사용한다!!
# core_models.TimeStampedModel은 사용안한다. DB에 저장해야하기떄문에
class User(AbstractUser):

    """ Custom User Model """

    GENDER_MALE = "male"
    GENDER_FMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FMALE, "Female"),
        (GENDER_OTHER, "Other"),
        # GENDER_~~ 가 DB로 갈 값이고, Male이 form에 보여질 속성이다.
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "kr"

    LANGUAGE_CHOICES = (
        (LANGUAGE_ENGLISH, "English"),
        (LANGUAGE_KOREAN, "Korean"),
    )

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"

    CURRENCY_CHOICES = (
        (CURRENCY_USD, "USD"),
        (CURRENCY_KRW, "KRW"),
    )

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_KAKAO = "kakao"
    LOGIN_CHOICES = (
        (LOGIN_EMAIL, "Email"),
        (LOGIN_GITHUB, "Github"),
        (LOGIN_KAKAO, "Kakao"),
    )

    avatar = models.ImageField(upload_to="avatars", null=True, blank=True)
    # blank ="true"는 form에서 빈공간을 빨간색표시하는데 저걸이용해 무시할수있다.
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    # 비어도 괜찮다!.. choices는 내장된 속성!! 3개의 값을 가지게 한다!

    bio = models.TextField(blank=True)
    bio2 = models.TextField(blank=True)
    # 여기에 뭘넣던 admin패널에 다생기게 된다. database에 넣을수있음
    # default값 은 무조껀 있어야 migrations 만든후 migrate 넘길수있다
    # 값을 뭐라도 넣어줘야 한다. 안그러면 db에 빈자리 처리가 안된다!
    # 또는 null=true 라고 적어줘서 빈칸 써도 된다고 해준다!!
    birthdate = models.DateField(blank=True, null=True)
    language = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=2, blank=True, default=LANGUAGE_KOREAN
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICES, max_length=3, blank=True, default=CURRENCY_KRW
    )
    superhost = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=20, default="", blank=True)
    # 이메일 시크릿은 유저가 아이디와 비번 만들면 시크릿 숫자를 추가할것이다!

    login_method = models.CharField(
        max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL
    )

    # user Detail 안에 있는 모델을 보기 위해서..URL을 반환 해야한다
    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})

    def verify_email(self):
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]  # 무작위 숫자 8진수후 20자리 가져오기!
            self.email_secret = secret
            html_message = render_to_string(
                "emails/verify_email.html", {"secret": secret}
            )
            # (f'To verify your account click <a href="http://localhost:8000/users/verify/{secret}">here</a>',)
            send_mail(
                # 여기서 중요한것은 message를 보낼때 텍스트는 택스트대로
                # html은 html 로 따로 보내야한다는 점이다! 그래서
                # 메시지를 html을 제외한 택스트 보내주는거 하나 strip_tags(html_message)
                # 메시지를 html만 뽑은거 하나를 보내주는것이다!
                "Verify Kwangwoo_BNB Account",
                strip_tags(html_message),  # html형태를 제외하고 return함
                # f'To verify your account click <a href="http://localhost:8000/users/verify/{secret}">here</a>',
                # string형태로 가서 href 가 안먹힐 것이다!
                settings.EMAIL_FROM,  # 세팅에서 들고옴!
                [self.email],  # 유저에게 보낸다!
                fail_silently=False,  # 애러 신경안쓴다!
                html_message=html_message,
            )
            self.save()  # 이과정을 다하고 저장한다!email_secret 같은것들이
        return

    # 모든 클래스는 밑의 매소드를 가지고 있다.
    # def __str__(self):
    #   return self.username