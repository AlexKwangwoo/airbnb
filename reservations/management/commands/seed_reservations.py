import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django_seed import Seed
from reservations import models as reservation_models
from users import models as user_models
from rooms import models as room_models

# from rooms import models as room_models 이렇게 하는게 좋다

NAME = "reservations"


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
            reservation_models.Reservation,
            number,
            {
                "status": lambda x: random.choice(["pending", "confirmed", "canceled"]),
                "guest": lambda x: random.choice(users),
                "room": lambda x: random.choice(rooms),
                "check_in": lambda x: datetime.now()
                + timedelta(days=random.randint(0, 7)),
                "check_out": lambda x: datetime.now()
                + timedelta(days=random.randint(10, 35)),
            },
        )  # check out 시간에는 좀더 기간을 램덤으로 정해서 넣어준다!

        seeder.execute()

        self.stdout.write(self.style.SUCCESS(f"{number} {NAME} created!!"))