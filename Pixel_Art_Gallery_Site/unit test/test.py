import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class FlaskLandingPageTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.get("http://localhost:5000")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_navigation_links(self):
        driver = self.driver
        links = driver.find_elements(By.CSS_SELECTOR, "nav ul li a")
        self.assertGreater(len(links), 0)
        for link in links:
            driver.execute_script("arguments[0].scrollIntoView();", link)
            link.click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "section")))
            self.assertTrue(driver.current_url.endswith(link.get_attribute("href").split("#")[-1]))

    def test_h1_tag_presence(self):
        driver = self.driver
        h1_tags = driver.find_elements(By.TAG_NAME, "h1")
        self.assertGreater(len(h1_tags), 0)

    def test_header_presence(self):
        driver = self.driver
        header = driver.find_element(By.TAG_NAME, "header")
        self.assertIsNotNone(header)

    def test_footer_presence(self):
        driver = self.driver
        footer = driver.find_element(By.TAG_NAME, "footer")
        self.assertIsNotNone(footer)

    def test_form_elements_presence(self):
        driver = self.driver
        h3 = driver.find_element(By.NAME, "h3")
        wrapper = driver.find_element(By.NAME, "wrapper")
        logo = driver.find_element(By.NAME, "logo")
        self.assertIsNotNone(h3)
        self.assertIsNotNone(wrapper)
        self.assertIsNotNone(logo)

    def test_details_tags_presence(self):
        driver = self.driver
        details_tags = driver.find_elements(By.TAG_NAME, "details")
        self.assertGreater(len(details_tags), 0)

if __name__ == "__main__":
    unittest.main()