import re

import allure

from data import ARRIVAL_TITLE_PATTERN, CAR_NUMBER_PATTERN, ORDER_ACTIONS, SEARCH_TITLE


@allure.feature("Заказ тарифа Такси: полный сценарий")
class TestTaxiOrderFlow:
    @allure.title("Рабочий со столиком: окно поиска, обратный отсчёт и кнопки")
    def test_search_window_elements_and_countdown(self, taxi_ride):
        assert taxi_ride.title() == SEARCH_TITLE
        assert taxi_ride.action_labels() == ORDER_ACTIONS
        assert taxi_ride.actions_are_enabled()
        assert taxi_ride.timer_is_in_header_right()
        before = taxi_ride.countdown_seconds()
        after = taxi_ride.wait_for_countdown_tick(before)
        assert 0 <= after < before

    @allure.title("Детали во время поиска содержат адреса и способ оплаты из формы")
    def test_search_details_match_order(self, taxi_ride, order_expectations):
        taxi_ride.open_details()
        details = taxi_ride.trip_details()
        assert details["origin"] == order_expectations["origin"]
        assert details["destination"] == order_expectations["destination"]
        assert details["payment"] == order_expectations["payment"]
        assert details["heading"] == "Еще про поездку"
        assert details["cost_label"].startswith("Стоимость")
        assert details["price"] == order_expectations["price"]

    @allure.title("После завершения поиска показаны машина и водитель")
    def test_assigned_order_elements(self, completed_ride, order_expectations):
        assert re.fullmatch(ARRIVAL_TITLE_PATTERN, completed_ride.title())
        assert completed_ride.action_labels() == ORDER_ACTIONS
        assert completed_ride.actions_are_enabled()
        car = completed_ride.assigned_car()
        assert re.fullmatch(CAR_NUMBER_PATTERN, car["number"], re.IGNORECASE)
        assert car["image"] == order_expectations["image"]
        assert car["image_loaded"]
        assert car["arrow_loaded"]
        assert car["number_on_right"]
        assert car["image_on_right"]
        driver_info = completed_ride.driver_information()
        assert driver_info["name"]
        assert driver_info["photo_loaded"]
        assert 0 <= driver_info["rating"] <= 5
        assert driver_info["rating_at_top_right"]

    @allure.title("Стоимость завершённого заказа совпадает с ценой выбранного тарифа")
    def test_completed_order_price(self, completed_ride, order_expectations):
        completed_ride.open_details()
        assert completed_ride.trip_details()["price"] == order_expectations["price"]

    @allure.title("Отмена завершённого заказа закрывает окно")
    def test_cancel_closes_order_window(self, completed_ride):
        completed_ride.cancel()
        assert completed_ride.is_closed()

    @allure.title("Полный флоу: Рабочий, столик, поиск, водитель, детали, отмена")
    def test_full_work_tariff_order_flow(self, taxi_ride, order_expectations):
        assert taxi_ride.title() == SEARCH_TITLE
        assert taxi_ride.action_labels() == ORDER_ACTIONS
        before = taxi_ride.countdown_seconds()
        assert taxi_ride.wait_for_countdown_tick(before) < before

        taxi_ride.wait_for_assignment()
        assert re.fullmatch(ARRIVAL_TITLE_PATTERN, taxi_ride.title())
        assert taxi_ride.assigned_car()["image"] == order_expectations["image"]
        assert taxi_ride.driver_information()["photo_loaded"]

        taxi_ride.open_details()
        details = taxi_ride.trip_details()
        assert details["origin"] == order_expectations["origin"]
        assert details["destination"] == order_expectations["destination"]
        assert details["payment"] == order_expectations["payment"]
        assert details["price"] == order_expectations["price"]

        taxi_ride.cancel()
        assert taxi_ride.is_closed()
