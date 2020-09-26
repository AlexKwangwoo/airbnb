from django import forms
from . import models


class CreateReviewForm(forms.ModelForm):
    accuracy = forms.IntegerField(max_value=5, min_value=1)
    communication = forms.IntegerField(max_value=5, min_value=1)
    cleanliness = forms.IntegerField(max_value=5, min_value=1)
    location = forms.IntegerField(max_value=5, min_value=1)
    check_in = forms.IntegerField(max_value=5, min_value=1)
    value = forms.IntegerField(max_value=5, min_value=1)

    class Meta:
        model = models.Review
        fields = (
            "review",
            "accuracy",
            "communication",
            "cleanliness",
            "location",
            "check_in",
            "value",
        )

    def save(self):
        review = super().save(commit=False)
        return review
        # view에서 form.is_valid()에서 review를 저장할수있게
        # 저장 방식을 바꾼다..
        # True로 안하는게.. 파이썬에서 객체를 생성하지만
        # db에 저장하는게 아니다!
        # view에서 form.is_valid()에서 review.save()를 통해 넣을것임!
