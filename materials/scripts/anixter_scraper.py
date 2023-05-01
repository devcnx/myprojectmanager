import materials.scripts.scraper_constants as sc
import time
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.utils import timezone
from materials.models import Material, MaterialVendor
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from urllib.parse import quote
from vendors.models import Vendor
from .scraper_base import Scraper


class AnixterScraper(Scraper):
    vendor: Vendor = Vendor.objects.get(vendor_id=1)
    material_vendor: MaterialVendor = None

    def __init__(self, email: str = sc.ANIXTER_LOGIN_EMAIL, password: str = sc.ANIXTER_LOGIN_PASSWORD):
        super().__init__(email, password)
        self.__email = email
        self.__password = password

    def create_chrome_driver_with_headers(self):
        self.__options = webdriver.ChromeOptions()
        self.__options.add_argument('--disable-extensions')
        self.__options.add_argument('--headless')
        # self.__options.add_argument('--incognito')
        self.__options.add_argument('--disable-gpu')
        self.__options.add_argument('--no-sandbox')
        self.__options.add_argument('--disable-dev-shm-usage')
        self.__options.add_argument(
            '--disable-blink-features=AutomationControlled')
        self.__options.add_argument(
            f'user-agent={sc.ANIXTER_USER_AGENT_ARRAY[0]}')

        self.__options.add_experimental_option(
            'prefs', {'profile.default_content_setting_values.automatic_downloads': 1})
        self.__options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        self.__options.add_experimental_option('useAutomationExtension', False)

        self.__driver = webdriver.Chrome(
            executable_path='./chromedriver', options=self.__options)

    def login(self):
        for attempt in range(3):
            self.__driver.get(sc.ANIXTER_BASE_URL + sc.ANIXTER_LOGIN_ENDPOINT)
            try:
                email_input = WebDriverWait(self.__driver, 5).until(
                    EC.presence_of_element_located((By.ID, sc.ANIXTER_EMAIL_INPUT_ID)))
                password_input = WebDriverWait(self.__driver, 5).until(
                    EC.presence_of_element_located((By.ID, sc.ANIXTER_PASSWORD_INPUT_ID)))
                if email_input and password_input:
                    email_input.send_keys(self.__email)
                    password_input.send_keys(self.__password)
                    password_input.send_keys(Keys.ENTER)
                    break
            except TimeoutException:
                if attempt < 2:
                    self.__driver.quit()
                    time.sleep(30)
                    self.__driver = self.create_chrome_driver_with_headers()
                    continue
                else:
                    self.__driver.quit()
                    current_date = datetime.now()
                    month = str(current_date.month).zfill(2)
                    day = str(current_date.day).zfill(2)
                    year = str(current_date.year)

                    hour = str(current_date.hour).zfill(2)
                    minute = str(current_date.minute).zfill(2)
                    second = str(current_date.second).zfill(2)

                    Scraper.email_update(
                        subject='ANIXTER SCRAPER LOGIN FAILED',
                        message=f'Failed to Login to {self.vendor.vendor_name.title()} at {hour}:{minute}:{second} on {month}-{day}-{year}\n\n'
                    )

    @staticmethod
    def create_new_material_vendors(new_materials, vendor):
        new_material_vendors = []
        for material in new_materials:
            # Create a new material vendor
            material_vendor = MaterialVendor.objects.create(
                material=material, vendor=vendor, vendor_description=material.description, vendor_part_number=material.manufacturer_number, vendor_unit_price=0.00, vendor_unit_of_measure='EA', vendor_product_link='www.product.com', vendor_image_link='www.image.com', last_modified=timezone.now(), last_modified_by=User.objects.get(username='automations'))
            new_material_vendors.append(material_vendor)
        return new_material_vendors

    def build_search_url(self):
        # Build the search url
        search_url = sc.ANIXTER_BASE_URL + \
            sc.ANIXTER_SEARCH_ENDPOINT + \
            quote(self.material_vendor.material.manufacturer_number)
        return search_url

    def is_search_page(self):
        return self.__driver.current_url == self.build_search_url()

    def find_product_url(self):
        try:
            elements = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'product-tile-tertiary')))
            for index, element in enumerate(elements):
                if self.material_vendor.material.manufacturer_number.upper() in element.text.upper():
                    element_text = elements[index].text
                    mfr_number = element_text.split('\n')[2].strip()
                    mfr_number = mfr_number.replace('MFR PART # ', '').strip()
                    if mfr_number.upper() == self.material_vendor.material.manufacturer_number.upper():
                        product_page_link = elements[index].find_element(By.CLASS_NAME, 'product-tile').find_element(
                            By.TAG_NAME, 'a').get_attribute('href')
                        return product_page_link
                    else:
                        continue
        except TimeoutException:
            return None

    def scrape(self):
        print(f'Starting the Anixter Scraper...')
        self.create_chrome_driver_with_headers()
        self.login()
        WebDriverWait(self.__driver, 10).until(
            EC.url_to_be(sc.ANIXTER_BASE_URL + sc.ANIXTER_HOME_ENDPOINT))
        print(f'Logged into {self.vendor.vendor_name.title()}')
        message = f'Logged into {self.vendor.vendor_name.title()} at {datetime.now().strftime("%H:%M:%S")} on {datetime.now().strftime("%m-%d-%Y")}\n\n'

        materials = Material.objects.all()

        material_vendors_to_update = [
            material_vendor for material_vendor in MaterialVendor.objects.filter()
        ]
