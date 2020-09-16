from django.db import models
from core import models as core_models

# Create your models here.
class Conversation(core_models.TimeStampedModel):
    """ Conversation Model Definition """

    participants = models.ManyToManyField(
        "users.User", related_name="conversations", blank=True
    )

    def __str__(self):
        usernames = []
        for user in self.participants.all():
            usernames.append(user.username)
        return ", ".join(usernames)
        # str은 date 타입이아니라 str타입으로 받을수만 있다!
        # return의 join은 리스트의 내용을 빈칸 한칸 간격으로 모아준다!

    def count_messages(self):
        return self.messages.count()
        # 밑의 클래스Message에서 갯수를 가져온다
        # many to many -> related_name="message" 이용해서!

    count_messages.short_description = "Number of Messages"

    def count_participants(self):
        return self.participants.count()
        # 본인 conversation 클래스 에서 갯수를 가져온다
        # 위의participants 속성을 이용해서!

    count_participants.short_description = "Number of Participants"


class Message(core_models.TimeStampedModel):
    """ Message Model Definition """

    message = models.TextField()
    user = models.ForeignKey(
        "users.User", related_name="messages", on_delete=models.CASCADE
    )
    conversation = models.ForeignKey(
        "Conversation", related_name="messages", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} says: {self.message}"
