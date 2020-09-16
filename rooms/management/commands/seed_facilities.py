from django.core.management.base import BaseCommand
from rooms.models import Facility

# from rooms import models as room_models 이렇게 하는게 좋다


class Command(BaseCommand):
    help = "This command creates facilities"
    # def add_arguments(self, parser)
    #     parser.add_argument(
    #         "--times", help="How many times do you want me to tell you that I Love you"
    #     )

    def handle(self, *args, **options):
        facilities = [
            "Private entrance",
            "Paid parking on premises",
            "Paid parking off premises",
            "Elevator",
            "Parking",
            "Gym",
        ]
        for f in facilities:
            Facility.objects.create(name=f)
            # Facility이 모듈이고 object를 가지고있고
            # 저기에 manager가 있고 생성하고 삭제 편집한다
            # 즉 위에 긴 내용을 facilities 저장해서
            # 각각의 f에 담아서 create를 해준다
            # Facility이 가지고 있는
            # name 속성에 추가할 것이다!
        self.stdout.write(self.style.SUCCESS(f"{len(facilities)} facilities created!!"))