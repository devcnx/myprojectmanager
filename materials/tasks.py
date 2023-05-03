from celery import shared_task, Celery
from django.core.mail import send_mail
from .scripts import graybar_scraper as gb, anixter_scraper as aw, cleaner as cl

app = Celery('myprojectmanager')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@shared_task
def run_graybar_scraper():
    scraper = gb.GraybarScraper()
    scraper.scrape()


# Run the task immediately.
run_graybar_scraper.delay()


@shared_task
def run_anixter_scraper():
    scraper = aw.AnixterScraper()
    scraper.scrape()


# Run the task immediately.
run_anixter_scraper.delay()


# @shared_task
# def clean_material_vendors():
#     cl.clean_material_vendors()


# Run the task immediately.
# clean_material_vendors.delay()
