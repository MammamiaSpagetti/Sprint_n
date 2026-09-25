import allure
import pytest

from data import ADDRESS_PAIRS, MAP_ADDRESS_LABELS


@allure.feature("Отрисовка маршрута")
class TestRouteRendering:
    @allure.title("На карте показаны начало и конец маршрута в правильном порядке")
    @pytest.mark.parametrize("route_addresses", ADDRESS_PAIRS, indirect=True, ids=("forward", "reverse"))
    def test_two_route_points_on_map(self, route_page, route_addresses):
        assert route_page.map_labels() == tuple(MAP_ADDRESS_LABELS[address] for address in route_addresses)
        start, end = route_page.map_pin_positions()
        assert (start["x"], start["y"]) != (end["x"], end["y"])
        layout = route_page.layout()
        assert layout["map"]["x"] >= layout["addresses"]["x"] + layout["addresses"]["width"]
