from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.contrib.auth.models import User
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
import time
from purbeurre.models.products import Products
from purbeurre.models.categories import Categories


class SeleniumTest(StaticLiveServerTestCase):
    """
    Simulates user behavior on website
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        cls.selenium = webdriver.Chrome(options=options)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(cls):
        cls.user = User.objects.create_user(username="test",
                                            first_name="test",
                                            password="password",
                                            email="test@user.fr")

        cls.category = Categories.objects.create(id=1, name="boisson")
        cls.product = Products.objects.create(name="noix de coco",
                                              nutriscore='c',
                                              image="https://static.openfoodfacts.org/images/products/541/004/100/1204/front_fr.97.400.jpg",
                                              category=Categories.objects.get
                                              (name=cls.category))

    def test_login(cls):
        """
        Takes user to login form with its data
        """
        cls.selenium.get('%s%s' % (cls.live_server_url, '/login/'))
        username_input = cls.selenium.find_element_by_name("email")
        username_input.send_keys('test@user.fr')
        password_input = cls.selenium.find_element_by_name("password")
        password_input.send_keys('password')
        try:
            time.sleep(1)
            cls.selenium.find_element_by_xpath('//input[@value="Connexion"]').click()
        except ElementClickInterceptedException:
            login_button = cls.selenium.find_element_by_xpath('//input[@value="Connexion"]')
            time.sleep(1)
            ActionChains(cls.selenium).move_to_element_with_offset(login_button, 0, -100).click().perform()

    def test_register_form(cls):
        """
        Simulates user registering his account
        """
        cls.selenium.get('%s%s' % (cls.live_server_url, '/register'))
        username_input = cls.selenium.find_element_by_name("email")
        username_input.send_keys('newuser@user.fr')
        username_input = cls.selenium.find_element_by_name("first_name")
        username_input.send_keys('User')
        password_input = cls.selenium.find_element_by_name("password")
        password_input.send_keys('Str0ngP@ssword')
        password_input = cls.selenium.find_element_by_name("password2")
        password_input.send_keys('Str0ngP@ssword')
        try:
            time.sleep(1)
            cls.selenium.find_element_by_xpath('//input[@value="S\'inscrire"]').click()
        except ElementClickInterceptedException:
            register_button = cls.selenium.find_element_by_xpath('//input[@value="S\'inscrire"]')
            time.sleep(1)
            ActionChains(cls.selenium).move_to_element_with_offset(register_button, 0, -100).click().perform()

    def test_search_form(cls):
        """
        Takes user to search form with a product name to put inside form
        """

        cls.selenium.get('%s%s' % (cls.live_server_url, '/'))
        form_input = cls.selenium.find_element_by_xpath \
            ('//div[@id="searchform"]/form[@role="form"]/input[@id="id_name"]')
        form_input.send_keys('noix de coco')
        form_input.send_keys(Keys.RETURN)

    def test_search_filter_form(cls):
        """
        Simulates user clicking on filter balise in index template, and
        then make its research with filters parameters
        """

        cls.selenium.get('%s%s' % (cls.live_server_url, '/'))
        filter_button = cls.selenium.find_element_by_xpath \
            ('//p[@id="filter_option"]')
        filter_button.click()
        name_input = cls.selenium.find_element_by_xpath \
            ('//div[@id="filter_name"]/input[@id="id_name"]')
        name_input.send_keys('coco')
        category_input = cls.selenium.find_element_by_xpath(
            '//select[@id="id_category"]/option[text()="boisson"]')
        category_input.click()
        nutriscore_input = cls.selenium.find_element_by_xpath(
            '//select[@id="id_nutriscore"]/option[text()="D"]')
        nutriscore_input.click()
        try:
            time.sleep(1)
            cls.selenium.find_element_by_xpath('//button[@id="search_filter_button"]').click()
        except ElementClickInterceptedException:
            search_button = cls.selenium.find_element_by_xpath('//button[@id="search_filter_button')
            time.sleep(1)
            ActionChains(cls.selenium).move_to_element_with_offset(search_button, 0, -100).click().perform()



