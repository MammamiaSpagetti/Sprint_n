import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators.taxi_ride_locators import TaxiRideLocators as L
from pages.base_page import BasePage


class TaxiRidePage(BasePage):
    def __init__(self, driver, timeout=20, search_timeout=90):
        super().__init__(driver, timeout)
        self._search_timeout = search_timeout

    @allure.step("Дождаться окна поиска и запуска обратного отсчёта")
    def wait_for_search(self):
        self._visible(L.DIALOG)
        self._wait.until(lambda _: self.countdown_seconds() > 0)
        return self

    def title(self):
        return self._text(L.TITLE)

    def action_labels(self):
        return self._texts(L.ACTION_LABELS)

    def actions_are_enabled(self):
        return self._enabled(L.CANCEL) and self._enabled(L.DETAILS_BUTTON)

    def countdown_seconds(self):
        minutes, seconds = self._text(L.TIMER).split(":")
        return int(minutes) * 60 + int(seconds)

    @allure.step("Дождаться уменьшения таймера поиска")
    def wait_for_countdown_tick(self, previous):
        self._wait.until(lambda _: self.countdown_seconds() < previous)
        return self.countdown_seconds()

    def timer_is_in_header_right(self):
        header, timer = self._rect(L.HEADER), self._rect(L.TIMER)
        return (timer["x"] > header["x"] + header["width"] / 2
                and header["y"] <= timer["y"] < header["y"] + header["height"])

    @allure.step("Дождаться завершения поиска машины")
    def wait_for_assignment(self):
        WebDriverWait(self._driver, self._search_timeout).until(
            EC.visibility_of_element_located(L.CAR_NUMBER)
        )
        self._visible(L.DRIVER_NAME)
        return self

    def assigned_car(self):
        header, number = self._rect(L.HEADER), self._rect(L.CAR_NUMBER)
        image = self._rect(L.CAR_IMAGE)
        return {
            "number": self._text(L.CAR_NUMBER),
            "image": self._visible(L.CAR_IMAGE).get_attribute("src"),
            "image_loaded": self._image_loaded(L.CAR_IMAGE),
            "arrow_loaded": self._image_loaded(L.TITLE_ARROW),
            "number_on_right": number["x"] > header["x"] + header["width"] / 2,
            "image_on_right": image["x"] > header["x"] + header["width"] / 2,
        }

    def driver_information(self):
        photo, rating = self._rect(L.DRIVER_PHOTO), self._rect(L.DRIVER_RATING)
        return {
            "name": self._text(L.DRIVER_NAME),
            "rating": float(self._text(L.DRIVER_RATING).replace(",", ".")),
            "photo_loaded": self._image_loaded(L.DRIVER_PHOTO),
            "rating_at_top_right": (
                rating["x"] >= photo["x"] + photo["width"] / 2
                and rating["y"] <= photo["y"] + photo["height"] / 2
            ),
        }

    @allure.step("Открыть детали поездки")
    def open_details(self):
        self._click(L.DETAILS_BUTTON)
        self._visible(L.TRIP_HEADING)

    def trip_details(self):
        return {
            "origin": self._text(L.detail_value("Адрес подачи")),
            "destination": self._text(L.detail_value("Адрес назначения")),
            "payment": self._text(L.detail_value("Способ оплаты")),
            "heading": self._text(L.TRIP_HEADING),
            "cost_label": self._text(L.TRIP_COST),
            "price": self._number(self._text(L.TRIP_COST)),
        }

    @allure.step("Отменить заказ")
    def cancel(self):
        self._click(L.CANCEL)

    def is_closed(self):
        return bool(self._wait.until(EC.invisibility_of_element_located(L.DIALOG)))
