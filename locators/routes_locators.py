from selenium.webdriver.common.by import By


class RoutesLocators:
    FROM = (By.ID, "from")
    TO = (By.ID, "to")
    ADDRESS_BLOCK = (By.CSS_SELECTOR, ".dst-picker")
    MAP = (By.ID, "map")
    MAP_LABELS = (By.CSS_SELECTOR, "#map [class$='route-pin__text']")
    START_PIN = (By.CSS_SELECTOR, "#map [class*='route-pin__label-0']")
    END_PIN = (By.CSS_SELECTOR, "#map [class*='route-pin__label-1']")
    ROUTE_BLOCK = (By.CSS_SELECTOR, ".type-picker.shown")
    MODES = (By.CSS_SELECTOR, ".type-picker .mode")
    ACTIVE_MODES = (By.CSS_SELECTOR, ".type-picker .mode.active")
    PRICE = (By.CSS_SELECTOR, ".type-picker .results-text .text")
    DURATION = (By.CSS_SELECTOR, ".type-picker .duration")
    CALL_TAXI = (By.XPATH, "//div[contains(@class,'type-picker')]//button[.='Вызвать такси']")
    BOOK_DRIVE = (By.XPATH, "//div[contains(@class,'type-picker')]//button[.='Забронировать']")
    TRANSPORT_ICONS = {
        "Машина": "car", "Пешком": "walk", "Такси": "taxi",
        "Велосипед": "bike", "Самокат": "scooter", "Драйв": "drive",
    }

    @staticmethod
    def mode(name):
        return By.XPATH, f"//div[@class='modes-container']/div[.='{name}']"

    @classmethod
    def transport(cls, name):
        icon = cls.TRANSPORT_ICONS[name]
        return By.XPATH, f"//div[@class='types-container']/div[img[contains(@src,'/media/{icon}')]]"
