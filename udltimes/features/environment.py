import os
import django
from behave.runner import Context
from splinter.browser import Browser
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'udlTimes_Web_Project.settings')


class ExtendedContext(Context):
    def get_url(self, to=None, *args, **kwargs):
        from django.urls import reverse
        from django.test import TestCase
        live_server_url = getattr(self.test, 'live_server_url', 'http://localhost')
        return live_server_url + (
            reverse(to, args=args, kwargs=kwargs) if to else '')


def before_all(context):
    django.setup()


def before_scenario(context, scenario):
    object.__setattr__(context, '__class__', ExtendedContext)

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')

    service = Service(ChromeDriverManager().install())
    context.browser = Browser('chrome', headless=True, service=service, options=chrome_options)


def after_scenario(context, scenario):
    if hasattr(context, 'browser'):
        try:
            context.browser.quit()
        except:
            pass


def after_all(context):
    pass