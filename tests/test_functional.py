from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.contrib.auth.models import User
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
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
        # options.add_argument('--headless')
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        cls.selenium = webdriver.Chrome(options=options)
        cls.selenium.implicitly_wait(10)

        cls.user = User.objects.create_user(username="test",
                                            first_name="test",
                                            password="password",
                                            email="test@user.fr")

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

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
            cls.selenium.find_element_by_xpath('//input[@value="Connexion"]').click()
            time.sleep(3)
        except Exception:
            login_button = cls.selenium.find_element_by_xpath('//input[@value="Connexion"]')
            ActionChains(cls.selenium).move_to_element_with_offset(login_button, 0, -100).click().perform()

    def test_search_form(cls):
        """
        Takes user to search form with a product name to put inside form
        """
        cls.category = Categories.objects.create(id=1, name="boisson")
        cls.product = Products.objects.create(name="noix de coco",
                                              nutriscore='c',
                                              image="https://static.openfoodfacts.org/images/products/541/004/100/1204/front_fr.97.400.jpg",
                                              category=Categories.objects.get
                                              (name=cls.category))
        cls.selenium.get('%s%s' % (cls.live_server_url, '/'))
        form_input = cls.selenium.find_element_by_xpath \
            ('//div[@id="searchform"]/form[@role="form"]/input[@id="id_research"]')
        form_input.send_keys('noix de coco')
        form_input.send_keys(Keys.RETURN)
        time.sleep(3)

    def test_search_filter_form(cls):
        """
        Simulates user clicking on filter balise in index template, and
        then make its research with filters parameters
        """
        cls.category = Categories.objects.create(id=1, name="boisson")
        cls.product = Products.objects.create(name="noix de coco",
                                              nutriscore='c',
                                              image="https://static.openfoodfacts.org/images/products/541/004/100/1204/front_fr.97.400.jpg",
                                              category=Categories.objects.get
                                              (name=cls.category))

        cls.selenium.get('%s%s' % (cls.live_server_url, '/'))
        filter_button = cls.selenium.find_element_by_xpath \
            ('//p[@id="filter_option"]')
        filter_button.click()
        name_input = cls.selenium.find_element_by_name("name")
        name_input.send_keys('coco')
        category_input = cls.selenium.find_element_by_xpath(
            '//select[@id="id_category"]/option[text()="boisson"]')
        category_input.click()
        time.sleep(2)
        nutriscore_input = cls.selenium.find_element_by_xpath(
            '//select[@id="id_nutriscore"]/option[text()="D"]')
        nutriscore_input.click()
        try:
            cls.selenium.find_element_by_xpath('//button[@id="search_filter_button"]').click()
            time.sleep(3)
        except Exception:
            search_button = cls.selenium.find_element_by_xpath('//button[@id="search_filter_button')
            time.sleep(5)
            ActionChains(cls.selenium).move_to_element_with_offset(search_button, 0, -100).click().perform()
