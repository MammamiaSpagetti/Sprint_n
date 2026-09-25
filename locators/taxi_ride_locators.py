from selenium.webdriver.common.by import By


class TaxiRideLocators:
    DIALOG = (By.CSS_SELECTOR, ".order.shown .order-body")
    HEADER = (By.CSS_SELECTOR, ".order.shown .order-header")
    TITLE = (By.CSS_SELECTOR, ".order.shown .order-header-title")
    TIMER = (By.CSS_SELECTOR, ".order.shown .order-header-time")
    CANCEL = (By.XPATH, "//div[contains(@class,'order-btn-group')][div[.='Отменить']]/button")
    DETAILS_BUTTON = (By.XPATH, "//div[contains(@class,'order-btn-group')][div[.='Детали']]/button")
    ACTION_LABELS = (By.XPATH, "//div[contains(@class,'order') and contains(@class,'shown')]//div[@class='order-btn-group'][button]/div")
    CAR_NUMBER = (By.CSS_SELECTOR, ".order.shown .order-number .number")
    CAR_IMAGE = (By.CSS_SELECTOR, ".order.shown .order-number img")
    TITLE_ARROW = (By.CSS_SELECTOR, ".order.shown .order-header-title img")
    DRIVER_NAME = (By.XPATH, "//div[@class='order-btn-group'][div[@class='order-button']]/div[last()]")
    DRIVER_PHOTO = (By.CSS_SELECTOR, ".order.shown div.order-button > img")
    DRIVER_RATING = (By.CSS_SELECTOR, ".order.shown .order-btn-rating")
    TRIP_HEADING = (By.XPATH, "//div[@class='order-details-content']/div[@class='o-d-h' and .='Еще про поездку']")
    TRIP_COST = (By.XPATH, "//div[@class='order-details-content'][div[.='Еще про поездку']]/div[@class='o-d-sh']")

    @staticmethod
    def detail_value(label):
        return By.XPATH, f"//div[@class='order-details-content'][div[@class='o-d-sh' and .='{label}']]/div[@class='o-d-h']"
