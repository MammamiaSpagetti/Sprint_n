import allure
import pytest

from data import ADDRESS_PAIRS, ROUTE_MODES, SAME_ADDRESS_PAIRS, SAME_ADDRESS_SUMMARY


@allure.feature("Блок выбора маршрута")
class TestRouteSelection:
    @allure.title("Блок выбора маршрута расположен под адресами")
    @pytest.mark.parametrize("route_addresses", ADDRESS_PAIRS, indirect=True, ids=("forward", "reverse"))
    def test_route_block_with_different_addresses(self, route_page):
        assert route_page.route_modes() == ROUTE_MODES
        layout = route_page.layout()
        assert layout["routes"]["y"] >= layout["addresses"]["y"] + layout["addresses"]["height"]

    @allure.title("Одинаковые адреса: Авто Бесплатно В пути 0 мин.")
    @pytest.mark.parametrize("route_addresses", SAME_ADDRESS_PAIRS, indirect=True, ids=("same-a", "same-b"))
    def test_free_zero_minute_route_with_same_addresses(self, route_page):
        assert route_page.route_modes() == ROUTE_MODES
        assert route_page.route_summary() == SAME_ADDRESS_SUMMARY
