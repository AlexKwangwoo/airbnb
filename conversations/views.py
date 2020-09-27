from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, reverse, render
from django.views.generic import View
from django.views.generic import TemplateView
from users import models as user_models
from reservations import models as reservation_models
from . import models, forms

# Create your views here.
def go_conversation(request, a_pk, b_pk):
    user_one = user_models.User.objects.get(pk=a_pk)
    user_two = user_models.User.objects.get(pk=b_pk)
    # room_ = room_models.Room.objects.get(pk=c_pk)

    if user_one is not None and user_two is not None:
        # conversation = models.Conversation.objects.filter(participants=user_one).filter(
        #     participants=user_two
        # )  먼저 유저 a가 있는 대화를 가져오고 유저 b 가 있는 대화를 가져올거임
        # 이거는 데이터 베이스에 효율적이지 않다
        try:
            conversation = models.Conversation.objects.get(
                Q(participants=user_one) & Q(participants=user_two)
            )  # 복잡한 쿼리를 다루는 경우... & | 쓸수있음.. 필터 하고..또 필터하는건 좋지 않다!
        except models.Conversation.DoesNotExist:
            conversation = models.Conversation.objects.create()
            conversation.participants.add(user_one, user_two)
        return redirect(reverse("conversations:detail", kwargs={"pk": conversation.pk}))


class ConversationDetailView(View):
    # detailview는 url의 pk를 찾을것이다!
    def get(self, *args, **kwargs):
        # 여기는 get방식을 통해 방을 찾을때
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404()
        # form = forms.AddCommentForm()
        # 폼안써서 form 필요없음
        return render(
            self.request,
            "conversations/conversation_detail.html",
            {"conversation": conversation},
            # 폼안써서 form 필요없음
            # {"conversation": conversation, "form": form},
        )

    def post(self, *args, **kwargs):
        # 여기는 post를 통해.. get으로 찾은곳의 response를 request할때!
        # 평범한 input 쓸꺼라..message에 ..필요없어짐!
        # form = forms.AddCommentForm(self.request.POST)
        # conversation detail의 form action을 통해 post를 받을 것임!
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404()
        message = self.request.POST.get("message", None)
        if message is not None:
            models.Message.objects.create(
                message=message, user=self.request.user, conversation=conversation
            )
        return redirect(reverse("conversations:detail", kwargs={"pk": pk}))


class ConversationView(TemplateView):
    template_name = "conversations/conversation.html"
