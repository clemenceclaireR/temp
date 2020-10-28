from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
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
        cls.selenium = WebDriver()
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

    def test_login(self):
        """
        Takes user to login form with its data
        """
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        username_input = self.selenium.find_element_by_name("email")
        username_input.send_keys('test@user.fr')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('password')
        try:
            self.selenium.find_element_by_xpath('//input[@value="Connexion"]').click()
        except Exception:
            pass
        #self.selenium.execute_script("arguments[0].click();", button)
        #validate = self.selenium.find_element_by_id('connexion')
        #validate.send_keys(Keys.RETURN)
        # WebDriverWait(self.selenium, 20).until(EC.visibility_of_element_located((By.XPATH,
        #                                                             '//input[@value="Connexion"]')))
        #
        # self.selenium.find_element_by_xpath('//input[@value="Connexion"]').click()

    def test_search_form(self):
        """
        Takes user to search form with a product name to put inside form
        """
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        form_input = self.selenium.find_element_by_id("id_research")
        form_input.send_keys('noix de coco')
        form_input.send_keys(Keys.RETURN)
