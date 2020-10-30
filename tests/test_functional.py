from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.contrib.auth.models import User
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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


    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    @classmethod
    def test_login(cls):
        """
        Takes user to login form with its data
        """
        cls.selenium.get('%s%s' % (cls.live_server_url, '/login/'))
        username_input = cls.selenium.find_element_by_name("email")
        username_input.send_keys('test@user.fr')
        password_input = cls.selenium.find_element_by_name("password")
        password_input.send_keys('password')
        cls.selenium.find_element_by_xpath('//input[@value="Connexion"]').click()

    @classmethod
    def test_search_form(cls):
        """
        Takes user to search form with a product name to put inside form
        """
        cls.selenium.get('%s%s' % (cls.live_server_url, '/'))
        form_input = cls.selenium.find_element_by_id("id_research")
        # form_input.send_keys('noix de coco')
        # self.selenium.find_element_by_xpath('//input[@id="chercher"]').click()
        #form_input.send_keys(Keys.RETURN)
