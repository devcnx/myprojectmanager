from abc import ABC, abstractmethod
from django.core.mail import send_mail


class Scraper(ABC):
    def __init__(self, email: str = '', password: str = ''):
        self.__email = email
        self.__password = password

    @abstractmethod
    def scrape(self):
        pass

    @staticmethod
    def email_update(subject: str = '', message: str = ''):
        send_mail(
            subject,
            message,
            'automations@upandcs.com',
            ['brittaney@upandcs.com'],
            fail_silently=False,
        )
