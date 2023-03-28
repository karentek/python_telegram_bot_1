import datetime

class Date:
    """Класс для конвертации строки в дату
    attributes:
        day (int): день
        month (int): месяц
        year (int): год
    return: None
    """
    def __init__(self, day: int = 0, month: int = 0, year: int = 0) -> None:
        self.day = day
        self.month = month
        self.year = year

    def __str__(self) -> str:
        return 'День {}\t Месяц {}\t Год {}\t'.format(
            self.day, self.month, self.year
        )

    @classmethod
    def is_date_valid(cls, day, month, year) -> bool:
        """
        Метод для проверки правильности написания даты
        attributes:
            date (str): дата введенная пользователем
        return: bool
        """
        current_date = datetime.date.today()

        return 0 < day < 32 and 0 < month < 13 and current_date.year <= year <= current_date.year + 1

    @classmethod
    def from_string(cls, date: str) -> 'Date':
        """
        Метод для конвертации строки в дату
        attributes:
            date (str): дата введенная пользователем
        return: объект класса Date
        """
        try:
            day, month, year = map(int, date.split('.'))
        except ValueError:
            day, month, year = map(int, date.split('-'))

        date_obj = cls(day, month, year)
        return date_obj


