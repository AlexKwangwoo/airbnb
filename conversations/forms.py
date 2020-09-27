from django import forms

# 사실상 필요없음 이제.. 그냥 input으로 대처 했음..
class AddCommentForm(forms.Form):
    message = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"placeholder": "Add a Comment"})
    )
