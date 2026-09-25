import allure
import pytest

from data import (
    CORRECT_DESCRIPTION_TARIFFS,
    ORDER_BUTTON_LABEL,
    ORDER_FORM_LABELS,
    SWAPPED_DESCRIPTION_TARIFFS,
    TARIFF_DESCRIPTIONS,
    TAXI_TARIFFS,
)


@allure.feature("Форма заказа такси")
class TestTaxiTariffs:
    @allure.title("В форме есть шесть тарифов и выбран ровно один")
    def test_six_tariffs_and_one_active(self, taxi_page):
        assert taxi_page.tariff_names() == TAXI_TARIFFS
        active = taxi_page.active_tariff_names()
        assert len(active) == 1
        assert active[0] in TAXI_TARIFFS

    @allure.title("Подсказка тарифа «{tariff}» соответствует ТЗ")
    @pytest.mark.parametrize("tariff", CORRECT_DESCRIPTION_TARIFFS)
    def test_tariff_description_on_hover(self, taxi_page, tariff):
        taxi_page.select_tariff(tariff)
        taxi_page.hover_tariff_info()
        assert taxi_page.tooltip() == (tariff, TARIFF_DESCRIPTIONS[tariff])

    @allure.title("Подсказка тарифа «{tariff}» соответствует ТЗ (BUG-001)")
    @pytest.mark.parametrize("tariff", SWAPPED_DESCRIPTION_TARIFFS)
    @pytest.mark.xfail(
        strict=True,
        raises=AssertionError,
        reason="BUG-001: на стенде перепутаны описания Сонного и Разговорчивого тарифов",
    )
    def test_sleepy_and_talkative_descriptions_match_specification(self, taxi_page, tariff):
        taxi_page.select_tariff(tariff)
        taxi_page.hover_tariff_info()
        assert taxi_page.tooltip() == (tariff, TARIFF_DESCRIPTIONS[tariff]), (
            "BUG-001: описание тарифа не соответствует ТЗ"
        )

    @allure.title("Под тарифами есть все поля заказа и кнопка отправки")
    def test_order_fields_below_tariffs(self, taxi_page):
        assert taxi_page.field_labels() == ORDER_FORM_LABELS
        assert taxi_page.fields_are_below_tariffs()
        assert taxi_page.comment_is_editable()
        assert taxi_page.submit_label() == ORDER_BUTTON_LABEL
