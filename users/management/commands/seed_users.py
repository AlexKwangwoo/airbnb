from django.core.management.base import BaseCommand
from django_seed import Seed
from users.models import User

# from rooms import models as room_models 이렇게 하는게 좋다


class Command(BaseCommand):
    help = "This command creates amenities"

    # argument 사용할때 이걸 쓴다!
    def add_arguments(self, parser):
        parser.add_argument(
            "--number",
            type=int,  # number를 int로 넘겨줘야 숫자로 받는다 기본은str
            default=2,
            help="How many users do you want to create?",
        )  # 없을때는 1을 입력한다!, --number은 argument로 밑에준다!

    def handle(self, *args, **options):
        number = options.get("number")  # 위에서 숫자를 들고온다!
        seeder = Seed.seeder()
        seeder.add_entity(
            User,  # User클래스에 있는 (컨트롤클릭해보셈..) 객체추가
            number,
            {
                "is_staff": False,
                "is_superuser": False,  # 이 두값들은 false설정해준다!
            },
        )  # 첫번째는 필드가 들어가고! 두번째는 갯수가들어간다!
        # number은 위에서 (argument를 받아오기위에 만들어짐) 받아온다!
        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} users created!!"))