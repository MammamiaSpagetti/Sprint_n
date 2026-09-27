import allure

from locators.taxi_order_locators import TaxiOrderLocators as L
from pages.base_page import BasePage


class TaxiOrderPage(BasePage):
    @allure.step("Дождаться открытия формы заказа такси")
    def wait_until_open(self):
        self._wait_for_panel(L.FORM)
        return self

    def tariff_names(self):
        return self._texts(L.TITLES)

    def active_tariff_names(self):
        return self._texts(L.ACTIVE_TITLES)

    @allure.step("Выбрать тариф «{name}»")
    def select_tariff(self, name):
        self._click(L.tariff(name))
        self._wait.until(lambda _: self.active_tariff_names() == (name,))

    @allure.step("Навести курсор на иконку информации выбранного тарифа")
    def hover_tariff_info(self):
        self._hover(L.INFO_BUTTON)
        self._visible(L.TOOLTIP)

    def tooltip(self):
        return self._text(L.TOOLTIP_TITLE), self._text(L.TOOLTIP_DESCRIPTION)

    def field_labels(self):
        return tuple(self._text(locator) for locator in (
            L.PHONE, L.PAYMENT_LABEL, L.COMMENT, L.REQUIREMENTS,
        ))

    def fields_are_below_tariffs(self):
        cards = self._wait.until(lambda d: d.find_elements(*L.CARDS))
        bottom = max(card.rect["y"] + card.rect["height"] for card in cards)
        return self._rect(L.PHONE)["y"] >= bottom

    def comment_is_editable(self):
        return self._enabled(L.COMMENT_INPUT)

    def submit_label(self):
        return self._text(L.SUBMIT_LABEL)

    def selected_price(self):
        return self._number(self._text(L.SELECTED_PRICE))

    def selected_image(self):
        return self._visible(L.SELECTED_IMAGE).get_attribute("src")

    def payment_method(self):
        return self._text(L.PAYMENT_VALUE)

    @allure.step("Включить требование «Столик для ноутбука»")
    def enable_laptop_table(self):
        self._click(L.REQUIREMENTS_HEADER)
        self._click(L.LAPTOP_SWITCH)

    def laptop_table_is_selected(self):
        return self._present(L.LAPTOP_CHECKBOX).is_selected()

    @allure.step("Нажать «Ввести номер и заказать»")
    def submit_order(self):
        self._click(L.SUBMIT)
