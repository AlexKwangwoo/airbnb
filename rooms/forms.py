from django import forms
from django_countries.fields import CountryField
from . import models


class SearchForm(forms.Form):

    city = forms.CharField(initial="Anywhere")  # widget=forms.Textarea 넣으면 형식이 바뀐다!
    country = CountryField(default="KR").formfield()
    room_type = forms.ModelChoiceField(
        required=False, empty_label="Any Kind", queryset=models.RoomType.objects.all()
    )
    price = forms.IntegerField(required=False)
    guests = forms.IntegerField(required=False)
    bedrooms = forms.IntegerField(required=False)
    beds = forms.IntegerField(required=False)
    baths = forms.IntegerField(required=False)
    instant_book = forms.BooleanField(required=False)
    superhost = forms.BooleanField(required=False)

    amenities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    facilities = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.Facility.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    house_rules = forms.ModelMultipleChoiceField(
        required=False,
        queryset=models.HouseRule.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )


class CreatePhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = (
            "caption",
            "file",
        )

    def save(self, pk, *args, **kwargs):
        # pk값을 가져올수 없기떄문에... view.py에서
        # AddPhotoView클래스 안에서 form_valid 안의 메소드에 pk인자를 받을수있게
        # 다시 만든다!
        photo = super().save(commit=False)
        room = models.Room.objects.get(pk=pk)
        photo.room = room
        photo.save()
        # saved된 method를 intercepting 하고있다!
        # 왜냐하면 url에 있는 pk를 가져와야해서!
        # 조금 어려워서 23.5페이지 참고!


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = models.Room
        fields = (
            "name",
            "description",
            "country",
            "city",
            "price",
            "address",
            "guests",
            "beds",
            "bedrooms",
            "baths",
            "check_in",
            "check_out",
            "room_type",
            "amenities",
            "facilities",
            "house_rules",
        )

    def save(self, *args, **kwargs):
        room = super().save(commit=False)
        # 커밋 false는 object는 만들지만 db에 저장하지 않는다
        # 여기서 CreateRoomview (view파일안) 안에서 form_valid로 넘겨준다!
        return room