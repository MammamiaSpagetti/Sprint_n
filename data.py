BASE_URL = "https://qa-routes.education-services.ru/"

ADDRESSES = ("Хамовнический Вал, 34", "Зубовский бульвар, 37")
ADDRESS_PAIRS = (ADDRESSES, tuple(reversed(ADDRESSES)))
SAME_ADDRESS_PAIRS = tuple((address, address) for address in ADDRESSES)
MAP_ADDRESS_LABELS = {
    "Хамовнический Вал, 34": "улица Хамовнический Вал, 34",
    "Зубовский бульвар, 37": "Зубовский бульвар, 37",
}

ROUTE_MODES = ("Оптимальный", "Быстрый", "Свой")
TRANSPORT_TYPES = ("Машина", "Пешком", "Такси", "Велосипед", "Самокат", "Драйв")
SAME_ADDRESS_SUMMARY = "Авто Бесплатно В пути 0 мин."

TAXI_TARIFFS = (
    "Рабочий", "Сонный", "Отпускной", "Разговорчивый", "Утешительный", "Глянцевый",
)
TARIFF_DESCRIPTIONS = {
    "Рабочий": "Для деловых особ, которых отвлекают",
    "Сонный": "Для тех, кто не выспался",
    "Отпускной": "Если пришла пора отдохнуть",
    "Разговорчивый": "Если мысли не выходят из головы",
    "Утешительный": "Если хочется свернуться калачиком",
    "Глянцевый": "Если нужно блистать",
}
CORRECT_DESCRIPTION_TARIFFS = ("Рабочий", "Отпускной", "Утешительный", "Глянцевый")
SWAPPED_DESCRIPTION_TARIFFS = ("Сонный", "Разговорчивый")
ORDER_FORM_LABELS = (
    "Телефон", "Способ оплаты", "Комментарий водителю...", "Требования к заказу",
)
ORDER_BUTTON_LABEL = "Ввести номер и заказать"
ORDER_ACTIONS = ("Отменить", "Детали")
SEARCH_TITLE = "Поиск машины"
ARRIVAL_TITLE_PATTERN = r"\d+ мин\. и приедет"
CAR_NUMBER_PATTERN = r"[а-яёa-z]\s*\d{3}\s*[а-яёa-z]{2}"
