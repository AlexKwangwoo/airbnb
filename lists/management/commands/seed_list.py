import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from lists import models as list_models
from users import models as user_models
from rooms import models as room_models

# from rooms import models as room_models 이렇게 하는게 좋다

NAME = "lists"


class Command(BaseCommand):
    help = f"This command creates {NAME}"

    # argument 사용할때 이걸 쓴다!
    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            type=int,  # number를 int로 넘겨줘야 숫자로 받는다 기본은str
            default=2,
            help=f"How many {NAME} do you want to create?",
        )  # 없을때는 1을 입력한다!, --number은 argument로 밑에준다!

    def handle(self, *args, **options):
        number = options.get("number")  # 위에서 숫자를 들고온다!
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()
        seeder.add_entity(
            list_models.List,
            number,
            {
                "user": lambda x: random.choice(users),
            },
        )  # 첫번째는 필드가 들어가고! 두번째는 갯수가들어간다!

        # number은 위에서 (argument를 받아오기위에 만들어짐) 받아온다!
        created = seeder.execute()  # -> 모든 룸을 creates photos에 넣는다!
        cleaned = flatten(list(created.values()))
        for pk in cleaned:
            list_model = list_models.List.objects.get(pk=pk)
            to_add = rooms[random.randint(0, 5) : random.randint(6, 30)]
            list_model.rooms.add(*to_add)
            # to_add는 쿼리셋이 되는데 *을 통해서
            # array 안의 요소를 가져올수있따

        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!!"))