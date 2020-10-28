import sys
from time import sleep

from selenium import webdriver
import unittest

import util

def screen():  # скриншот
    Test.test_fullpage_screenshot(unittest.TestCase)  # делаем скриншот
    Test.tearDown(unittest.TestCase)


class Test(unittest.TestCase):
    """ Demonstration: Get Chrome to generate fullscreen screenshot """
    def tearDown(self):
        self.driver.quit()

    def test_fullpage_screenshot(self):
        ''' Generate document-height screenshot '''
        #url = "http://effbot.org/imagingbook/introduction.htm"
        url = "http://www.musicmen-dv.ru/repetition/online.php"
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.get(url)
        sleep(2)
        util.fullpage_screenshot(self.driver, "table.png")

if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]])
