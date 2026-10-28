import allure


@allure.step("Проверяем статус {expected}")
def assert_status(response, expected=200):
    assert response.status_code == expected, \
        f"Ожидали {expected}, получили {response.status_code}: {response.text}"


@allure.step("Проверяем, что сервер вернул ошибку {codes}")
def assert_error(response, codes=(400, 404, 405, 500)):
    assert response.status_code in codes, \
        f"Ожидали ошибку из {codes}, получили {response.status_code}: {response.text}"
