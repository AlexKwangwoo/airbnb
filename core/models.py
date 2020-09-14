from django.db import models

# Create your models here.
class TimeStampedModel(models.Model):
    """ Time Stamped Model"""

    created = models.DateTimeField(auto_now_add=True)
    # 장고가 새로운 model을
    # 만들때 날짜를 알아서 기록 해준다

    updated = models.DateTimeField(auto_now=True)
    # 장고가 모델이 업데이트(저장) 될때마다 날짜를 기록해준다

    class Meta:  # abstract 는 db로 가지 않는다!
        abstract = True
