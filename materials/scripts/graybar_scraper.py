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


class GraybarScraper(Scraper):
    vendor: Vendor = Vendor.objects.get(vendor_id=3)
    material_vendor: MaterialVendor = None

    def __init__(self, email: str = sc.GRAYBAR_LOGIN_EMAIL, password: str = sc.GRAYBAR_LOGIN_PASSWORD):
        super().__init__(email, password)
        self.__email = email
        self.__password = password

    def create_chrome_driver_with_headers(self):
        self.__options = Options()
        self.__options.add_argument('--disable-web-security')
        self.__options.add_argument('--user-data-dir=some_temp_folder')
        self.__options.add_argument('--disable-extensions')
        self.__options.add_argument('--disable-gpu')
        self.__options.add_argument('--no-sandbox')
        self.__options.add_argument('--disable-dev-shm-usage')
        self.__options.add_argument(
            '--disable-blink-features=AutomationControlled')
        self.__options.add_argument('--headless')
        # self.__options.add_argument('--incognito')

        self.__options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        self.__options.add_experimental_option('useAutomationExtension', False)
        self.__driver = webdriver.Chrome(
            options=self.__options, executable_path='/usr/local/bin/chromedriver')
        self.__options.add_experimental_option(
            'prefs', {'profile.default_content_setting_values.automatic_downloads': 1})

        for key, value in sc.GRAYBAR_HEADERS.items():
            self.__options.add_argument(f'{key}={value}')

        self.__driver = webdriver.Chrome(options=self.__options)

    def check_for_popup(self):
        try:
            popup = WebDriverWait(self.__driver, 5).until(
                EC.presence_of_element_located((By.XPATH, sc.GRAYBAR_POPUP_XPATH)))
            if popup:
                popup.click()
        except TimeoutException:
            pass

    def login(self):
        self.__driver.get(sc.GRAYBAR_BASE_URL + sc.GRAYBAR_LOGIN_ENDPOINT)
        self.check_for_popup()
        try:
            email_input = WebDriverWait(self.__driver, 5).until(
                EC.presence_of_element_located((By.ID, sc.GRAYBAR_EMAIL_INPUT_ID)))
            password_input = WebDriverWait(self.__driver, 5).until(
                EC.presence_of_element_located((By.ID, sc.GRAYBAR_PASSWORD_INPUT_ID)))
            if email_input and password_input:
                email_input.send_keys(self.__email)
                password_input.send_keys(self.__password)
                password_input.send_keys(Keys.ENTER)
        except TimeoutException:
            self.__driver.quit()
            Scraper.email_update(
                subject='GRAYBAR SCRAPER LOGIN FAILED',
                message=f'Failed to Login to {self.vendor.vendor_name.title()} at {datetime.now()}',
            )
            # Stop the script from running
            raise SystemExit

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
        search_url = sc.GRAYBAR_BASE_URL + \
            sc.GRAYBAR_SEARCH_ENDPOINT + \
            quote(self.material_vendor.material.manufacturer_number)
        return search_url

    def is_search_page(self):
        return self.__driver.current_url == self.build_search_url()

    def find_product_url(self):
        try:
            elements = WebDriverWait(self.__driver, 5).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'product-listing_product')))
            if elements:
                for index, element in enumerate(elements):
                    if self.material_vendor.material.manufacturer_number.lower().strip() in element.text.lower().strip():
                        element_text = elements[index].text
                        try:
                            matches = element_text.split('\n')
                            if matches[5].lower().strip() == self.material_vendor.material.manufacturer_number.lower().strip():
                                return elements[index].find_element(By.TAG_NAME, 'a').get_attribute('href')
                        except IndexError:
                            return None
        except TimeoutException:
            return None

    def scrape(self):
        print(f'Starting the Graybar Scraper...')
        self.create_chrome_driver_with_headers()
        self.login()
        WebDriverWait(self.__driver, 10).until(
            EC.url_to_be(sc.GRAYBAR_BASE_URL + sc.GRAYBAR_HOME_ENDPOINT))
        if self.__driver.current_url != sc.GRAYBAR_BASE_URL + sc.GRAYBAR_HOME_ENDPOINT:
            print(
                f'Failed to Login to {self.vendor.vendor_name.title()} at {datetime.now()}')
            self.__driver.quit()
            Scraper.email_update(
                subject='GRAYBAR SCRAPER LOGIN FAILED',
                message=f'Failed to Login to {self.vendor.vendor_name.title()} at {datetime.now()}',
            )
            # Stop the script until the next scheduled run
            raise SystemExit
        print(
            f'Successfully Logged into {self.vendor.vendor_name.title()} at {datetime.now()}')
        message = f'Successfully Logged into {self.vendor.vendor_name.title()} at {datetime.now()}\n\n'

        materials = Material.objects.all()
        # If the material vendor hasn't been updated in the last (7) days, has None as a value for the last_modified
        # field, doesn't exist, or the material vendor's vendor_part_number is the same as the material's
        # manufacturer_number, then the material vendor needs to be updated.
        material_vendors_to_update = [material_vendor for material_vendor in MaterialVendor.objects.filter(
            vendor=self.vendor) if material_vendor.last_modified == None or material_vendor.last_modified < timezone.now() - timedelta(days=7) or material_vendor.vendor_part_number.lower() == material_vendor.material.manufacturer_number.lower() or material_vendor.vendor_product_link == 'www.product.com' or material_vendor.vendor_unit_price == 0.00]
        number_of_vendors_to_update = len(material_vendors_to_update)

        message += f'{number_of_vendors_to_update} Material Vendors to Update\n\n'

        # Get a list of new materials that don't have a material vendor
        new_materials = [material for material in materials if not MaterialVendor.objects.filter(
            material=material, vendor=self.vendor).exists()]
        number_of_new_materials = len(new_materials)

        message += f'{number_of_new_materials} New Materials to Add\n\n'

        new_material_vendors = self.create_new_material_vendors(
            new_materials, self.vendor)

        # Update the material vendors
        material_vendors_to_update.extend(new_material_vendors)

        for index, material_vendor in enumerate(material_vendors_to_update, start=1):
            # Set the material vendor
            self.material_vendor = material_vendor

            message += f'{index} of {number_of_vendors_to_update} | {self.material_vendor.material.description}\n'

            # Navigate to the vendor_product_link if it exists. Otherwise, build the URL to search for the product.
            if self.material_vendor.vendor_product_link and self.material_vendor.vendor_product_link is not None and self.material_vendor.vendor_product_link not in ['www.product.com', 'n/a', 'na', 'none', '']:
                self.__driver.get(self.material_vendor.vendor_product_link)
            else:
                self.__driver.get(self.build_search_url())

            # Check for the popup
            self.check_for_popup()

            # If the current url is the search url, then find the product url
            if self.is_search_page():
                product_url = self.find_product_url()
                if product_url:
                    self.__driver.get(product_url)
                else:
                    print(
                        f'Failed to find the product url for {self.material_vendor.material.description} at {datetime.now()}')
                    message += f'Failed to find the product url for {self.material_vendor.material.description} at {datetime.now()}\n\n'
                    continue

            # Check for the popup
            self.check_for_popup()

            # Get the product description
            try:
                product_details = WebDriverWait(self.__driver, 5).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'product-details')))
                if product_details:
                    description = product_details[1].text.split('\n')[1]
                    # Replace any character that aren't letters, numbers, or dashes.
                    description = ''.join(
                        [character for character in description if character.isalnum() or character == '-' or character.isspace()])
                    if description:
                        self.material_vendor.vendor_description = description

                        message += f'Vendor Description : {description}\n'
            except TimeoutException:
                # self.material_vendor.vendor_description = self.material_vendor.material.description
                pass

            # Get the vendor part number
            vendor_part_number = product_details[1].text.split('\n')[
                3].replace('SKU: ', '')
            if vendor_part_number:
                print(
                    f'{index} of {number_of_vendors_to_update} | {vendor_part_number}')

                message += f'Vendor Part Number : {vendor_part_number}\n'

                self.material_vendor.vendor_part_number = vendor_part_number

            # Get the vendor unit price and unit of measure
            try:
                pricing = WebDriverWait(self.__driver, 5).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'pdpbox')))
                if pricing:
                    pricing_and_uom = [
                        element.text for element in pricing if element.text != '']
                    if 'Call for Pricing' in pricing_and_uom:
                        message += f'Vendor Unit Price : Call for Pricing\n'
                        self.material_vendor.vendor_unit_price = 0.00
                        message += f'Vendor Unit of Measure : EA\n'
                        self.material_vendor.vendor_unit_of_measure = 'EA'
                    else:
                        pricing_and_uom = pricing_and_uom[0].split('\n')[0]
                        pricing_and_uom = pricing_and_uom.split('/') if '/' in pricing_and_uom else [
                            pricing_and_uom]
                        if len(pricing_and_uom) == 2:
                            try:
                                vendor_unit_price = float(pricing_and_uom[0].replace(
                                    '$', '').replace(',', '')) if pricing_and_uom[0] else 0.00
                                vendor_unit_of_measure = pricing_and_uom[1].strip().lower(
                                ) if pricing_and_uom[1] else 'ea'
                                message += f'Vendor Unit Price : {vendor_unit_price}\n'
                                self.material_vendor.vendor_unit_price = vendor_unit_price
                                message += f'Vendor Unit of Measure : {vendor_unit_of_measure}\n'
                                self.material_vendor.vendor_unit_of_measure = vendor_unit_of_measure
                            except ValueError:
                                pass

            except TimeoutException:
                pass

            # Get the vendor image link
            try:
                main_image = WebDriverWait(self.__driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'mainImage')))
                if main_image:
                    image_link = main_image.get_attribute('src')
                    if image_link and image_link != "https://www.graybar.com/_ui/responsive/theme-alpha/images/missing_product_en_300x300.jpg":
                        message += f'Vendor Image Link : {image_link}\n'
                        self.material_vendor.vendor_image_link = image_link
                    else:
                        message += f'Vendor Image Link : None\n'
                        self.material_vendor.vendor_image_link = 'n/a'
            except TimeoutException:
                pass

            # Get the vendor product link
            self.material_vendor.vendor_product_link = self.__driver.current_url
            message += f'Vendor Product Link : {self.material_vendor.vendor_product_link}\n'

            # Save the material vendor
            self.material_vendor.save()

            message += '\n'

            # Wait for 5 seconds
            time.sleep(5)

        # Quit the driver
        self.__driver.quit()

        # Send the email
        Scraper.email_update(
            subject='GRAYBAR SCRAPER UPDATE',
            message=message,
        )

        print(f'Graybar Scraper Complete')
