from django.core.management.base import BaseCommand
from rooms.models import Amenity

# from rooms import models as room_models 이렇게 하는게 좋다


class Command(BaseCommand):
    help = "This command creates amenities"
    # def add_arguments(self, parser)
    #     parser.add_argument(
    #         "--times", help="How many times do you want me to tell you that I Love you"
    #     )

    def handle(self, *args, **options):
        amenities = [
            "Air conditioning",
            "Alarm Clock",
            "Balcony",
            "Bathroom",
            "Bathtub",
            "Bed Linen",
            "Boating",
            "Cable TV",
            "Carbon monoxide detectors",
            "Chairs",
            "Children Area",
            "Coffee Maker in Room",
            "Cooking hob",
            "Cookware & Kitchen Utensils",
            "Dishwasher",
            "Double bed",
            "En suite bathroom",
            "Free Parking",
            "Free Wireless Internet",
            "Freezer",
            "Fridge / Freezer",
            "Golf",
            "Hair Dryer",
            "Heating",
            "Hot tub",
            "Indoor Pool",
            "Ironing Board",
            "Microwave",
            "Outdoor Pool",
            "Outdoor Tennis",
            "Oven",
            "Queen size bed",
            "Restaurant",
            "Shopping Mall",
            "Shower",
            "Smoke detectors",
            "Sofa",
            "Stereo",
            "Swimming pool",
            "Toilet",
            "Towels",
            "TV",
        ]
        for a in amenities:
            Amenity.objects.create(name=a)
            # Amenitiy가 모듈이고 object를 가지고있고
            # 저기에 manager가 있고 생성하고 삭제 편집한다
            # 즉 위에 긴 내용을 amenities에 저장해서
            # 각각의 a에 담아서 create를 해준다
            # Amenity가 가지고 있는
            # name 속성에 추가할 것이다!
        self.stdout.write(self.style.SUCCESS("Amenities created!!"))