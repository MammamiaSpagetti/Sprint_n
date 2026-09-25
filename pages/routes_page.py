import allure

from locators.routes_locators import RoutesLocators as L
from pages.base_page import BasePage


class RoutesPage(BasePage):
    @allure.step("Открыть страницу маршрутов")
    def open(self, url):
        self._driver.get(url)
        self._visible(L.FROM)
        return self

    @allure.step("Построить маршрут: {origin} → {destination}")
    def set_addresses(self, origin, destination):
        self._fill(L.FROM, origin)
        self._fill(L.TO, destination)
        self._wait_for_panel(L.ROUTE_BLOCK)

    @allure.step("Прочитать подписи начала и конца маршрута на карте")
    def map_labels(self):
        self._visible(L.START_PIN)
        self._visible(L.END_PIN)
        self._wait.until(lambda d: len(d.find_elements(*L.MAP_LABELS)) == 2)
        return self._texts(L.MAP_LABELS)

    def map_pin_positions(self):
        return self._rect(L.START_PIN), self._rect(L.END_PIN)

    def layout(self):
        return {
            "addresses": self._rect(L.ADDRESS_BLOCK),
            "routes": self._rect(L.ROUTE_BLOCK),
            "map": self._rect(L.MAP),
        }

    def route_modes(self):
        return self._texts(L.MODES)

    def active_modes(self):
        return self._texts(L.ACTIVE_MODES)

    def route_summary(self):
        return f"{self._text(L.PRICE)} {self._text(L.DURATION)}"

    def route_information(self):
        return {
            "price": self._number(self._text(L.PRICE)),
            "minutes": self._number(self._text(L.DURATION)),
        }

    @allure.step("Выбрать вид маршрута «{name}»")
    def select_mode(self, name):
        self._click(L.mode(name))
        self._wait.until(lambda _: self.active_modes() == (name,))

    def transport_is_enabled(self, name):
        return self._enabled(L.transport(name))

    @allure.step("Выбрать тип передвижения «{name}»")
    def select_transport(self, name):
        self._click(L.transport(name))

    def transport_is_active(self, name):
        return "active" in self._visible(L.transport(name)).get_attribute("class").split()

    def call_taxi_is_enabled(self):
        return self._enabled(L.CALL_TAXI)

    def book_drive_is_enabled(self):
        return self._enabled(L.BOOK_DRIVE)

    @allure.step("Нажать «Вызвать такси»")
    def call_taxi(self):
        self._click(L.CALL_TAXI)
