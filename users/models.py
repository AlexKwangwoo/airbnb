from django.contrib.auth.models import AbstractUser

# 유저파트는 위에것을 import 해서 사용할것이다..

from django.db import models

# Create your models here.
# 장고 속의 models속의 class Model을 사용한다!!
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

    avatar = models.ImageField(null=True, blank=True)
    # blank ="true"는 form에서 빈공간을 빨간색표시하는데 저걸이용해 무시할수있다.
    gender = models.CharField(
        choices=GENDER_CHOICES, max_length=10, null=True, blank=True
    )
    # 비어도 괜찮다!.. choices는 내장된 속성!! 3개의 값을 가지게 한다!

    bio = models.TextField(default="", blank=True)
    # 여기에 뭘넣던 admin패널에 다생기게 된다. database에 넣을수있음
    # default값 은 무조껀 있어야 migrations 만든후 migrate 넘길수있다
    # 값을 뭐라도 넣어줘야 한다. 안그러면 db에 빈자리 처리가 안된다!
    # 또는 null=true 라고 적어줘서 빈칸 써도 된다고 해준다!!
    birthdate = models.DateField(null=True)

    language = models.CharField(
        choices=LANGUAGE_CHOICES, max_length=2, null=True, blank=True
    )

    currency = models.CharField(
        choices=CURRENCY_CHOICES, max_length=3, null=True, blank=True
    )

    superhost = models.BooleanField(default=False)
