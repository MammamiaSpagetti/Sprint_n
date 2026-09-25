# Приёмы исследования и автоматизации интерфейса

## setTimeout в консоли

Чтобы успеть навести курсор на подсказку перед остановкой JavaScript, в DevTools Console можно выполнить:

```javascript
setTimeout(() => { debugger; }, 3000);
```

Затем выбрать тариф и навести курсор на `i`. Через заданный интервал DevTools остановит выполнение; открытый элемент можно изучить во вкладке Elements. Продолжение выполнения — `F8`.

`setTimeout` планирует вызов функции и сразу возвращает управление; фактическая задержка может быть больше указанной. Это инструмент ручного исследования. В автотестах таймер приложения не подменяется, поиск машины проходит естественно. См. [описание setTimeout на MDN](https://developer.mozilla.org/en-US/docs/Web/API/Window/setTimeout).

## Наведение в Selenium

В Selenium Python наведение выполняется через `ActionChains(driver).move_to_element(element).perform()`. Метод `_hover` в `BasePage` сначала дожидается видимости элемента. `TaxiOrderPage.hover_tariff_info` после наведения ждёт видимую подсказку. См. [Mouse actions в документации Selenium](https://www.selenium.dev/documentation/webdriver/actions_api/mouse/).

На этом стенде кнопка информации скрыта у неактивных карточек: перед наведением выбирается нужный тариф. Проверяется видимый текст, а не содержимое скрытого tooltip в DOM.

## xfail

`@pytest.mark.xfail` обозначает известное расхождение, но тест продолжает исполняться. В проекте `strict=True` обнаруживает неожиданный успех, а `raises=AssertionError` ограничивает ожидаемое падение проверкой результата. Ошибка Selenium остаётся обычной ошибкой прогона.

`--runxfail` отключает обработку маркеров для конкретного запуска. Так можно одновременно сохранить требуемую пометку в коде и получить Allure-отчёт с настоящими падениями. См. [документацию pytest о xfail](https://docs.pytest.org/en/stable/how-to/skipping.html) и [интеграцию Allure с pytest](https://allurereport.org/docs/pytest/).
