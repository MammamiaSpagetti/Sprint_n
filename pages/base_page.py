import re

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver, timeout=20):
        self._driver = driver
        self._timeout = timeout
        self._wait = WebDriverWait(driver, timeout)

    def _visible(self, locator):
        return self._wait.until(EC.visibility_of_element_located(locator))

    def _present(self, locator):
        return self._wait.until(EC.presence_of_element_located(locator))

    def _click(self, locator):
        self._wait.until(EC.element_to_be_clickable(locator)).click()

    def _fill(self, locator, text):
        element = self._visible(locator)
        element.send_keys(Keys.CONTROL, "a", Keys.BACKSPACE)
        element.send_keys(text, Keys.TAB)

    def _text(self, locator):
        return self._visible(locator).text.strip()

    def _texts(self, locator):
        elements = self._wait.until(EC.visibility_of_all_elements_located(locator))
        return tuple(element.text.strip() for element in elements)

    def _wait_for_panel(self, locator):
        self._visible(locator)
        self._wait.until(lambda _: self._visible(locator).value_of_css_property("opacity") == "1")

    def _hover(self, locator):
        ActionChains(self._driver).move_to_element(self._visible(locator)).perform()

    def _enabled(self, locator):
        element = self._visible(locator)
        return element.is_enabled() and "disabled" not in element.get_attribute("class").split()

    def _image_loaded(self, locator):
        image = self._visible(locator)
        self._wait.until(lambda _: image.get_property("complete"))
        return image.get_property("naturalWidth") > 0

    def _rect(self, locator):
        return self._visible(locator).rect

    @staticmethod
    def _number(text):
        return int(re.search(r"\d+", text).group())
