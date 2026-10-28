
Автотесты для сущностей pet, store, user (Swagger Petstore, базовый URL https://petstore.swagger.io/v2).

- Для каждого из 20 запросов API: один позитивный и один негативный тест.
- Pydantic: модели данных (`models.py`).
- Allure: декораторы feature, story, severity на каждом тесте.
- `base_request.py`: базовый класс для запросов.

Готовый отчёт лежит в файле `allure-report.html` (одиночный HTML).
Чтобы открыть, скачайте файл и откройте в браузере.

pip install -r requirements.txt
pytest -v --alluredir=allure-results
