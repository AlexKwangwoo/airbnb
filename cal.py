from django.utils import timezone
import calendar


class Day:
    # 이 Day는 밑의 Calendar에서 객체가 생성된다!!
    def __init__(self, number, past, month, year):
        self.number = number
        self.past = past
        self.month = month
        self.year = year

    def __str__(self):
        return str(self.number)


class Calendar(calendar.Calendar):
    def __init__(self, year, month):
        super().__init__(firstweekday=6)
        self.year = year
        self.month = month
        self.day_names = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")
        self.months = (
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        )

    def get_days(self):
        weeks = self.monthdays2calendar(self.year, self.month)
        # 한주한주의 모든 정보를 가져온다.. 만약
        # 일 월 화 수 목 금 토
        # 0  0  1  2  3  4  5
        # 이면.. 첫번째는 (0,6),(0,1),(1,2) 이런식.. 첫번째 인자는 날짜
        # 두번째 인자는 요일.. 일요일은 6 월요일은 1이다..
        #  결국 그 달에 해당하는 주를 가져온다.. 보통 1주부터 5주까지!
        days = []
        for week in weeks:
            for day, _ in week:
                # 두번째 인자로 주고싶은게 없으면 _ 를 쓰면된다
                now = timezone.now()
                today = now.day
                month = now.month
                past = False
                if month == self.month:
                    if day <= today:
                        past = True
                new_day = Day(number=day, past=past, month=self.month, year=self.year)
                # day<today는 생성자의 past를 나타낸다!
                # 여기서 Day!!를 만든다!!
                days.append(new_day)
        return days

    def get_month(self):
        return self.months[self.month - 1]
