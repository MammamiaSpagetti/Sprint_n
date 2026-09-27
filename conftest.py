import json
import os
import platform
from pathlib import Path

import allure
import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service

from data import ADDRESS_PAIRS, BASE_URL
from pages.routes_page import RoutesPage
from pages.taxi_order_page import TaxiOrderPage
from pages.taxi_ride_page import TaxiRidePage


def pytest_addoption(parser):
    parser.addoption("--base-url", default=os.getenv("BASE_URL", BASE_URL))
    parser.addoption("--headed", action="store_true", help="Показать окно Chrome")
    parser.addoption("--ui-timeout", type=float, default=20)
    parser.addoption("--search-timeout", type=float, default=90)


@pytest.fixture
def _browser(request):
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1600,1200")
    if not request.config.getoption("--headed"):
        options.add_argument("--headless=new")
    if os.getenv("CHROME_BINARY"):
        options.binary_location = os.environ["CHROME_BINARY"]
    service = Service(executable_path=os.getenv("CHROMEDRIVER"))
    browser = webdriver.Chrome(service=service, options=options)
    request.config.browser_version = browser.capabilities["browserVersion"]
    browser.set_page_load_timeout(60)
    try:
        yield browser
    finally:
        browser.quit()


@pytest.fixture
def routes_page(_browser, request):
    page = RoutesPage(_browser, request.config.getoption("--ui-timeout"))
    return page.open(request.config.getoption("--base-url"))


@pytest.fixture
def route_addresses(request):
    return getattr(request, "param", ADDRESS_PAIRS[0])


@pytest.fixture
def route_page(routes_page, route_addresses):
    origin, destination = route_addresses
    routes_page.set_addresses(origin, destination)
    return routes_page


@pytest.fixture
def taxi_page(_browser, route_page, request):
    route_page.select_mode("Быстрый")
    route_page.call_taxi()
    return TaxiOrderPage(_browser, request.config.getoption("--ui-timeout")).wait_until_open()


@pytest.fixture
def work_tariff(taxi_page):
    taxi_page.select_tariff("Рабочий")
    taxi_page.enable_laptop_table()
    assert taxi_page.laptop_table_is_selected(), "Не включён столик для ноутбука"
    return taxi_page


@pytest.fixture
def order_expectations(work_tariff, route_addresses):
    return {
        "origin": route_addresses[0],
        "destination": route_addresses[1],
        "payment": work_tariff.payment_method(),
        "price": work_tariff.selected_price(),
        "image": work_tariff.selected_image(),
    }


@pytest.fixture
def taxi_ride(_browser, work_tariff, order_expectations, request):
    work_tariff.submit_order()
    return TaxiRidePage(
        _browser,
        request.config.getoption("--ui-timeout"),
        request.config.getoption("--search-timeout"),
    ).wait_for_search()


@pytest.fixture
def completed_ride(taxi_ride):
    return taxi_ride.wait_for_assignment()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    browser = item.funcargs.get("_browser")
    if browser is not None and (report.when == "call" or report.failed):
        try:
            allure.attach(
                browser.get_screenshot_as_png(),
                name=f"{report.when}: {report.outcome}",
                attachment_type=allure.attachment_type.PNG,
            )
            if report.failed or hasattr(report, "wasxfail"):
                allure.attach(
                    browser.page_source,
                    name="HTML страницы при расхождении",
                    attachment_type=allure.attachment_type.HTML,
                )
        except WebDriverException as error:
            allure.attach(str(error), name="Ошибка сохранения диагностики")


def pytest_sessionfinish(session, exitstatus):
    results_dir = session.config.getoption("allure_report_dir", default=None)
    if results_dir and not session.config.option.collectonly:
        results = Path(results_dir)
        results.mkdir(parents=True, exist_ok=True)
        environment = {
            "URL": session.config.getoption("--base-url"),
            "Browser": "Chrome",
            "Browser.Version": getattr(session.config, "browser_version", "not started"),
            "Python": platform.python_version(),
            "OS": platform.platform(),
            "Run.Xfail.As.Failures": str(session.config.getoption("runxfail")),
        }
        (results / "environment.properties").write_text(
            "\n".join(f"{key}={value}" for key, value in environment.items()),
            encoding="utf-8",
        )
        (results / "categories.json").write_text(json.dumps([
            {
                "name": "BUG-001: перепутаны описания тарифов",
                "matchedStatuses": ["failed"],
                "messageRegex": ".*BUG-001.*",
            },
        ], ensure_ascii=False), encoding="utf-8")
