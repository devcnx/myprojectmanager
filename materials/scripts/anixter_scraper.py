import materials.scripts.scraper_constants as sc
import time
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.utils import timezone
from materials.models import Material, MaterialAlternativeManufacturerNumber, MaterialVendor
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

    def get_product_details(self, material_vendor):
        try:
            product_details = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'product-heading'))).find_elements(By.TAG_NAME, 'span')
            product_details = [detail.text for detail in product_details]
            description = product_details[1]
            if description:
                material_vendor.vendor_description = description
            else:
                material_vendor.vendor_description = material_vendor.material.description

            vendor_part_number = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'col-sm-7')))
            vendor_part_number = [detail.text for detail in vendor_part_number.find_elements(
                By.TAG_NAME, 'span')][3].replace('PART # ', '').strip()
            if vendor_part_number:
                material_vendor.vendor_part_number = vendor_part_number.lower()
            else:
                material_vendor.vendor_part_number = material_vendor.material.manufacturer_number.lower()

            vendor_unit_price = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'js-priceDisplay'))).text
            if vendor_unit_price:
                try:
                    vendor_unit_price = float(
                        vendor_unit_price.replace('$', '').replace(',', ''))
                    material_vendor.vendor_unit_price = vendor_unit_price
                except ValueError:
                    # If the existing vendor_unit_price is 0.00 or > 0.00, keep it.
                    if material_vendor.vendor_unit_price >= 0.00:
                        pass
                    else:
                        material_vendor.vendor_unit_price = 0.00
            else:
                if material_vendor.vendor_unit_price >= 0.00:
                    pass
                else:
                    material_vendor.vendor_unit_price = 0.00

            vendor_unit_of_measure = WebDriverWait(self.__driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'product-measurement'))).text
            if vendor_unit_of_measure:
                if '/' in vendor_unit_of_measure:
                    vendor_unit_of_measure = vendor_unit_of_measure.replace(
                        '/', '').strip()
                if any(unit in vendor_unit_of_measure.lower() for unit in ['pack', 'roll', 'box', 'each', 'pair']):
                    vendor_unit_of_measure = 'ea'
                if 'thousand each' in vendor_unit_of_measure.lower():
                    vendor_unit_of_measure = '1000ea'
                if 'thousand feet' in vendor_unit_of_measure.lower():
                    vendor_unit_of_measure = '1000ft'
                material_vendor.vendor_unit_of_measure = vendor_unit_of_measure.lower().strip()
            else:
                material_vendor.vendor_unit_of_measure = 'ea'

            vendor_product_link = self.__driver.current_url
            if vendor_product_link:
                material_vendor.vendor_product_link = vendor_product_link
            else:
                # If the material vendor already has a vendor_product_link, keep it.
                if material_vendor.vendor_product_link.lower() not in ['', 'www.product.com', 'n/a', 'na', 'none']:
                    pass
                else:
                    material_vendor.vendor_product_link = 'www.product.com'

            # Check if the material vendor has a vendor_image_link that isn't n/a, na, none, www.image.com, or https://www.anixter.com/_ui/desktop/theme-green/images/missing-product-250x250.jpg.
            # If it does, keep it. Otherwise, scrape the vendor_image_link.
            if material_vendor.vendor_image_link.lower() not in ['', 'www.image.com', 'n/a', 'na', 'none', 'https://www.anixter.com/_ui/desktop/theme-green/images/missing-product-250x250.jpg']:
                pass
            else:
                vendor_image_link = WebDriverWait(self.__driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'productImagePrimary'))).get_attribute('src')
                if vendor_image_link and vendor_image_link != 'https://www.anixter.com/_ui/desktop/theme-green/images/missing-product-250x250.jpg':
                    material_vendor.vendor_image_link = vendor_image_link
                else:
                    material_vendor.vendor_image_link = 'www.image.com'

        except TimeoutException:
            pass

        material_vendor.last_modified = timezone.now()
        material_vendor.last_modified_by = User.objects.get(
            username='automations')
        material_vendor.save()

    def handle_direct_link(self, material_vendors_with_direct_link):
        for material_vendor in material_vendors_with_direct_link:
            self.__driver.get(material_vendor.vendor_product_link)
            try:
                WebDriverWait(self.__driver, 10).until(
                    EC.url_to_be(material_vendor.vendor_product_link))
                self.get_product_details(material_vendor)
            except TimeoutException:
                continue

    def handle_search(self, material_vendors_that_require_search):
        for material_vendor in material_vendors_that_require_search:
            self.material_vendor = material_vendor
            self.__driver.get(self.build_search_url())
            try:
                WebDriverWait(self.__driver, 10).until(
                    EC.url_to_be(self.build_search_url()))
                if self.is_search_page():
                    product_page_link = self.find_product_url()
                    if product_page_link:
                        self.__driver.get(product_page_link)
                        try:
                            WebDriverWait(self.__driver, 10).until(
                                EC.url_to_be(product_page_link))
                            self.get_product_details(material_vendor)
                        except TimeoutException:
                            continue
                    else:
                        # Check if there's an alternative manufacturer number for the material.
                        alternative_manufacturer_numbers = MaterialAlternativeManufacturerNumber.objects.filter(
                            material=material_vendor.material)
                        # If there are alternative manufacturer numbers, loop through them and search for each one.
                        # If a product page link is found, break out of the loop and scrape the product details.
                        # If no product page link is found, continue to the next material vendor.
                        if alternative_manufacturer_numbers:
                            for alternative in alternative_manufacturer_numbers:
                                self.__driver.get(sc.ANIXTER_BASE_URL + sc.ANIXTER_SEARCH_ENDPOINT + quote(
                                    alternative.alternative_manufacturer_number))
                                try:
                                    WebDriverWait(self.__driver, 10).until(
                                        EC.url_to_be(sc.ANIXTER_BASE_URL + sc.ANIXTER_SEARCH_ENDPOINT + quote(
                                            alternative.alternative_manufacturer_number)))
                                    if self.is_search_page():
                                        product_page_link = self.find_product_url()
                                        if product_page_link:
                                            self.__driver.get(
                                                product_page_link)
                                            try:
                                                WebDriverWait(self.__driver, 10).until(
                                                    EC.url_to_be(product_page_link))
                                                self.get_product_details(
                                                    material_vendor)
                                                break
                                            except TimeoutException:
                                                continue
                                        else:
                                            continue
                                    else:
                                        self.get_product_details(
                                            material_vendor)
                                        break
                                except TimeoutException:
                                    continue
                        else:
                            # If there are no alternative manufacturer numbers, and the material vendor doesn't have
                            # a valid vendor_product_link, continue to the next material vendor.
                            continue
                else:
                    self.get_product_details(material_vendor)
            except TimeoutException:
                continue

    def scrape(self):
        print(f'Starting the Anixter Scraper...')
        self.create_chrome_driver_with_headers()
        self.login()
        WebDriverWait(self.__driver, 10).until(
            EC.url_to_be(sc.ANIXTER_BASE_URL + sc.ANIXTER_HOME_ENDPOINT))
        print(f'Logged into {self.vendor.vendor_name.title()}')
        message = f'Logged into {self.vendor.vendor_name.title()} on {datetime.now().strftime("%m/%d/%Y %H:%M:%S")}\n\n'

        materials = Material.objects.all()

        material_vendors = MaterialVendor.objects.filter(vendor=self.vendor)
        print(f'({len(material_vendors)}) Existing Anixter Material Vendors')
        message += f'({len(material_vendors)}) Existing Anixter Material Vendors\n'

        material_vendors_to_create = [material for material in materials if not MaterialVendor.objects.filter(
            material=material, vendor=self.vendor).exists()]
        number_of_material_vendors_to_create = len(material_vendors_to_create)
        print(
            f'({number_of_material_vendors_to_create}) Anixter Material Vendors to Create')
        message += f'({number_of_material_vendors_to_create}) Anixter Material Vendors to Create\n\n'

        new_material_vendors = self.create_new_material_vendors(
            material_vendors_to_create, self.vendor)

        material_vendors_to_update = []

        for material_vendor in material_vendors:
            if material_vendor.last_modified == None or \
                material_vendor.last_modified < timezone.now() - timedelta(days=7) or \
                material_vendor.vendor_part_number.lower().strip() == material_vendor.material.manufacturer_number.lower().strip() or \
                material_vendor.vendor_unit_price == 0.00 or \
                    material_vendor.vendor_product_link.lower() in ['', 'www.product.com', 'n/a', 'na', 'none']:
                material_vendors_to_update.append(material_vendor)
        material_vendors_to_update.extend(new_material_vendors)
        number_of_material_vendors_to_update = len(material_vendors_to_update)
        print(
            f'({number_of_material_vendors_to_update}) Anixter Material Vendors to Update')
        message += f'\n({number_of_material_vendors_to_update}) Anixter Material Vendors to Update\n\n'

        Scraper.email_update(
            subject='ANIXTER SCRAPER STARTED',
            message=message
        )

        message = ''
        with_direct_link = []
        requires_search = []
        for index, material_vendor in enumerate(material_vendors_to_update, start=1):
            # Check if the material vendor has a vendor_product_link. If it does, add it to the with_direct_link list.
            if material_vendor.vendor_product_link.lower() not in ['', 'www.product.com', 'n/a', 'na', 'none', None]:
                with_direct_link.append(material_vendor)
            else:
                # If the material vendor does not have a valid vendor_product_link, add it to the requires_search list.
                requires_search.append(material_vendor)

        print(f'({len(with_direct_link)}) Anixter Material Vendors with Direct Links')
        message += f'({len(with_direct_link)}) Anixter Material Vendors with Direct Links\n\n'

        print(
            f'({len(requires_search)}) Anixter Material Vendors that Require Search')
        message += f'({len(requires_search)}) Anixter Material Vendors that Require Search\n\n'

        Scraper.email_update(
            subject='ANIXTER SCRAPER UPDATE',
            message=message
        )
        # self.handle_direct_link(with_direct_link)
        self.handle_search(requires_search)
