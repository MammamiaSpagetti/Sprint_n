import allure
import pytest

from data import ADDRESS_PAIRS, TRANSPORT_TYPES


@allure.feature("Подготовка к заказу такси")
class TestTaxiPreparation:
    @allure.title("Переключение Оптимальный → Быстрый → Оптимальный обновляет маршрут")
    @pytest.mark.parametrize("route_addresses", ADDRESS_PAIRS, indirect=True, ids=("forward", "reverse"))
    def test_switch_route_mode_recalculates_information(self, route_page):
        route_page.select_mode("Оптимальный")
        assert route_page.active_modes() == ("Оптимальный",)
        optimal = route_page.route_information()

        route_page.select_mode("Быстрый")
        assert route_page.active_modes() == ("Быстрый",)
        fast = route_page.route_information()
        assert fast["price"] != optimal["price"]
        assert 0 < fast["minutes"] <= optimal["minutes"]

        route_page.select_mode("Оптимальный")
        assert route_page.active_modes() == ("Оптимальный",)
        assert route_page.route_information() == optimal

    @allure.title("Свой: можно выбрать тип передвижения {transport}")
    @pytest.mark.parametrize("transport", TRANSPORT_TYPES)
    def test_custom_mode_enables_transport_types(self, route_page, transport):
        route_page.select_mode("Свой")
        assert route_page.active_modes() == ("Свой",)
        assert route_page.transport_is_enabled(transport)
        route_page.select_transport(transport)
        assert route_page.transport_is_active(transport)

    @allure.title("Для быстрого маршрута активна кнопка «Вызвать такси»")
    def test_fast_mode_enables_call_taxi(self, route_page):
        route_page.select_mode("Быстрый")
        assert route_page.call_taxi_is_enabled()

    @allure.title("Свой → Драйв: активна кнопка «Забронировать»")
    def test_custom_drive_enables_booking(self, route_page):
        route_page.select_mode("Свой")
        route_page.select_transport("Драйв")
        assert route_page.transport_is_active("Драйв")
        assert route_page.book_drive_is_enabled()
