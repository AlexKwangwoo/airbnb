import random
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from django_seed import Seed
from rooms import models as room_models
from users import models as user_models

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
        all_users = user_models.User.objects.all()  # 이것과 밑에게 포린키로못받아와서
        room_types = room_models.RoomType.objects.all()  # 이것을 함께 랜덤함수로 뽑아준다!
        seeder.add_entity(
            room_models.Room,  # room_models파일에 Room클래스에 있는 (컨트롤클릭해보셈..) 객체추가
            number,
            {
                "name": lambda x: seeder.faker.address(),
                "host": lambda x: random.choice(all_users),
                "room_type": lambda x: random.choice(room_types),
                "price": lambda x: random.randint(1, 300),
                "guests": lambda x: random.randint(1, 20),
                "beds": lambda x: random.randint(1, 5),
                "bedrooms": lambda x: random.randint(1, 5),
                "baths": lambda x: random.randint(1, 5),
            },
        )  # 첫번째는 필드가 들어가고! 두번째는 갯수가들어간다!

        # number은 위에서 (argument를 받아오기위에 만들어짐) 받아온다!
        created_photos = seeder.execute()  # -> 모든 룸을 creates photos에 넣는다!
        created_clean = flatten(list(created_photos.values()))
        # flatten은 [[14]] 와같은 리스트속 리스트(이상한모양에서)
        # 요약된 [14]만 가져와준다!
        amenities = room_models.Amenity.objects.all()
        facilities = room_models.Facility.objects.all()
        rules = room_models.HouseRule.objects.all()
        # 다대 다를 넣기위한방법!!
        for pk in created_clean:  # 생성된 모든 룸(created_clean 리스트의 형태)
            room = room_models.Room.objects.get(pk=pk)
            # 프라이머리 키로 룸을 찾고 (들어갈 룸!!)
            # 왼쪽 pk는 방의 id가 될것이고, 오른쪽 pk는 created_clean의 인자들이 될것이다!
            for i in range(3, random.randint(10, 30)):  # min 3 ~ max (10~30)의 사진생성
                room_models.Photo.objects.create(
                    caption=seeder.faker.sentence(),
                    room=room,  # 왼쪽룸은 photo의룸 오른쪽은 바로 위의 room이 될것이다!
                    file=f"room_photos/{random.randint(1,45)}.webp",  # 문제생기면 9.4 다시보기
                    # file="room_photos/31.jpg", 문제생기면 여기를 고치자!! 사진도 확장자 jpg로 바꿔야함!
                    # 다운로드하고 파일을 여는경우가 생긴다.. jpg는 괜찮음!
                )
            for a in amenities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.amenities.add(a)
            for f in facilities:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.facilities.add(f)
            for r in rules:
                magic_number = random.randint(0, 15)
                if magic_number % 2 == 0:
                    room.house_rules.add(r)
        self.stdout.write(self.style.SUCCESS(f"{number} rooms created!!"))