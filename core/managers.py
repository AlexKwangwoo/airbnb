from django.db import models

# reservation의 managers 가 다른데도 쓰일수있기에 코어에 만듬!
class CustomModelManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None
