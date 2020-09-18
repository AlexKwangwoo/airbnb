import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from reviews import models as review_models
from users import models as user_models
from rooms import models as room_models

# from rooms import models as room_models 이렇게 하는게 좋다


class Command(BaseCommand):
    help = "This command creates amenities"

    # argument 사용할때 이걸 쓴다!
    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            type=int,  # number를 int로 넘겨줘야 숫자로 받는다 기본은str
            default=2,
            help="How many rooms do you want to create?",
        )  # 없을때는 1을 입력한다!, --number은 argument로 밑에준다!

    def handle(self, *args, **options):
        number = options.get("number")  # 위에서 숫자를 들고온다!
        seeder = Seed.seeder()
        users = user_models.User.objects.all()
        rooms = room_models.Room.objects.all()
        seeder.add_entity(
            review_models.Review,
            number,
            {
                "accuracy": lambda x: random.randint(0, 6),
                "communication": lambda x: random.randint(0, 6),
                "cleanliness": lambda x: random.randint(0, 6),
                "location": lambda x: random.randint(0, 6),
                "check_in": lambda x: random.randint(0, 6),
                "value": lambda x: random.randint(0, 6),
                "room": lambda x: random.choice(rooms),
                "user": lambda x: random.choice(users),
            },
        )  # 첫번째는 필드가 들어가고! 두번째는 갯수가들어간다!

        # number은 위에서 (argument를 받아오기위에 만들어짐) 받아온다!
        seeder.execute()  # -> 모든 룸을 creates photos에 넣는다!
        self.stdout.write(self.style.SUCCESS(f"{number} reviews created!!"))