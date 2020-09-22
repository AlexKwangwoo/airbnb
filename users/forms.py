from django import forms
from . import models

# from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    # email = forms.EmailField()
    # password = forms.CharField(widget=forms.PasswordInput)
    # 장고의 input을 바꾸는 방법은 밑에 방법뿐이다..placeholder
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )

    def clean(self):
        email = self.cleaned_data.get("email")
        # cleaned_data는 사용자가 입력한 데이터를 뜻한다.
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            # 그리고 찾는다! username과 email이 같다면!

            # clean과 같이 모든걸 하나에 넣으면 필드 하나하나마다 명확하게 에러를
            # 표시해줘야 한다!!! 밑에 페스워드 처럼!!
            if user.check_password(password):
                return self.cleaned_data
            else:
                # add_error("필드이름!!", 일어날수있는 에러!!)
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))


# class SignUpForm(UserCreationForm):
#     username = forms.EmailField(label="Email")
# 요거 18강 마지막 이거 해볼랬는데.. signup에서 자꾸 오류떠서 다시 월래대로 감!
# 결국 바꾼건.. 밑에꺼랑 요거다!


# ------------------- form.modelform을 usercreationForm으로 바꿨따.. 보고싶으면 주석 전체 해제하면됨
# -----중요!! modelForm은 결국 커스터마이징이 쉽지않아
class SignUpForm(forms.ModelForm):
    # forms.Form은 저장을한다..즉 signup결과를 저장할수있다
    class Meta:  # modelform이 알아서 중복 이메일이 있는지 검사한다!
        # 클래스 이름도 바뀌면 안됨!!
        model = models.User
        fields = ("first_name", "last_name", "email")
        # 여기에 추가하면 회원가입 양식을 늘리는것이다 ex) "birthdate"
        # fields가 있을때 widgets 바꾸는법은 밑에 있다!
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last Name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email Name"}),
        }

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"})
    )
    # password = forms.CharField(widget=forms.PasswordInput)
    # password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    # ------------------------------------------------------------------
    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)  # find User 있다면 밑의 줄 실행!
            raise forms.ValidationError(
                "That email is already taken", code="existing_user"
            )
        except models.User.DoesNotExist:  # 유저가 없으면 이 애러가 뜨고 email리턴!
            return email

    # ------------- 필요없다 왜냐하면 modelForm이 알아서 clean 시킬꺼다!

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")

        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:  # 패스워드 같으면 패스워드 리턴!
            return password

    # 세이브 메쏘드 없어도 저장 자체가 되는 클래스 이다!!!!!!!!!!!
    # 하지만 유저 이름이 없다.. 이메일로 쓰기 때문에.. 그래서 다시 만든다!
    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        # commit=False는 장고user object는 만들어지지만
        # 데이터베이스에 저장은 하지 말라는 뜻임
        user.username = email
        # email이 결국 username이 된다!
        user.set_password(password)
        user.save()


# -----------------------------------------------------------------------
# -----------------------------------------------------------------------

# signupform을 좀더 쉽게 modelform으로 위에서 바꿀꺼다!
# class SignUpForm(forms.Form):  # forms.Form은 저장을한다..즉 signup결과를 저장할수있다

#     first_name = forms.CharField(max_length=80)
#     last_name = forms.CharField(max_length=80)
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput)
#     password1 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

#     def clean_email(self):
#         email = self.cleaned_data.get("email")
#         try:
#             models.User.objects.get(email=email)  # find User 있다면 밑의 줄 실행!
#             raise forms.ValidationError("User already exists with")
#         except models.User.DoesNotExist:  # 유저가 없으면 이 애러가 뜨고 email리턴!
#             return email

#     def clean_password1(self):
#         password = self.cleaned_data.get("password")
#         password1 = self.cleaned_data.get("password1")

#         if password != password1:
#             raise forms.ValidationError("Password confirmation does not match")
#         else:  # 패스워드 같으면 패스워드 리턴!
#             return password

#     def save(self):
#         first_name = self.cleaned_data.get("first_name")
#         last_name = self.cleaned_data.get("last_name")
#         email = self.cleaned_data.get("email")
#         password = self.cleaned_data.get("password")

#         # models.User.object.create() 이거는 사용못함 왜냐하면 비번이 암호화되기때문
#         user = models.User.objects.create_user(email, email, password)
#         # user를 생성 한다.. 암호화된 비번과 함께
#         user.first_name = first_name
#         user.last_name = last_name
#         user.save()

# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
# def clean_email(self):
#     # email을 정리하는것이다!! user가 보낸 데이터에서 email을 갖는것!
#     # clean_ 은 정해진것이다.. 뭔가 정리하고싶을때! 에러내거나또는 정리!!
#     # 데이터를 받으면 장고가 검사하고.. 그다음 cleaned_data를 보내줌!
#     # return안하면 field를 다지워버린다!
#     email = self.cleaned_data.get("email")
#     try:
#         models.User.objects.get(username=email)
#         # 그리고 찾는다! username과 email이 같다면!
#         return email
#     except models.User.DoesNotExist:
#         raise forms.ValidationError("User does not exist")

# def clean_password(self):
#     email = self.cleaned_data.get("email")
#     password = self.cleaned_data.get("password")
#     try:
#         user = models.User.objects.get(username=email)
#         # 그리고 찾는다! username과 email이 같다면!
#         if user.check_password(password):
#             return password
#         else:
#             raise forms.ValidationError("Password is wrong")
#     except models.User.DoesNotExist:
#         raise forms.ValidationError("User does not exist")
