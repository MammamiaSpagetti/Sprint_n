from selenium.webdriver.common.by import By


class TaxiOrderLocators:
    FORM = (By.CSS_SELECTOR, ".tariff-picker.shown")
    CARDS = (By.CSS_SELECTOR, ".tariff-picker.shown .tcard")
    TITLES = (By.CSS_SELECTOR, ".tariff-picker.shown .tcard-title")
    ACTIVE_TITLES = (By.CSS_SELECTOR, ".tariff-picker.shown .tcard.active .tcard-title")
    SELECTED_PRICE = (By.CSS_SELECTOR, ".tariff-picker.shown .tcard.active .tcard-price")
    SELECTED_IMAGE = (By.CSS_SELECTOR, ".tariff-picker.shown .tcard.active .tcard-icon img")
    INFO_BUTTON = (By.CSS_SELECTOR, ".tariff-picker.shown .tcard.active .tcard-i")
    TOOLTIP = (By.CSS_SELECTOR, ".tariff-picker.shown .tcard.active .__react_component_tooltip.show")
    TOOLTIP_TITLE = (By.CSS_SELECTOR, ".tariff-picker.shown .tcard.active .__react_component_tooltip.show .i-title")
    TOOLTIP_DESCRIPTION = (By.CSS_SELECTOR, ".tariff-picker.shown .tcard.active .__react_component_tooltip.show .i-dPrefix")
    PHONE = (By.CSS_SELECTOR, ".tariff-picker.shown .np-text")
    PAYMENT_LABEL = (By.CSS_SELECTOR, ".tariff-picker.shown .pp-text")
    PAYMENT_VALUE = (By.CSS_SELECTOR, ".tariff-picker.shown .pp-value-text")
    COMMENT = (By.CSS_SELECTOR, ".tariff-picker.shown label[for='comment']")
    COMMENT_INPUT = (By.CSS_SELECTOR, ".tariff-picker.shown #comment")
    REQUIREMENTS = (By.CSS_SELECTOR, ".tariff-picker.shown .reqs-head")
    REQUIREMENTS_HEADER = (By.CSS_SELECTOR, ".tariff-picker.shown .reqs-header")
    LAPTOP_SWITCH = (By.XPATH, "//div[contains(@class,'tariff-picker') and contains(@class,'shown')]//div[@class='r-sw-container'][div[.='Столик для ноутбука']]//span[contains(@class,'slider')]")
    LAPTOP_CHECKBOX = (By.XPATH, "//div[contains(@class,'tariff-picker') and contains(@class,'shown')]//div[@class='r-sw-container'][div[.='Столик для ноутбука']]//input")
    SUBMIT = (By.CSS_SELECTOR, ".smart-button")
    SUBMIT_LABEL = (By.CSS_SELECTOR, ".smart-button-main")

    @staticmethod
    def tariff(name):
        return By.XPATH, f"//div[contains(@class,'tariff-picker') and contains(@class,'shown')]//div[contains(@class,'tcard')][div[@class='tcard-title' and .='{name}']]"
