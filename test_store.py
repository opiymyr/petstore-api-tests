import allure
from base_request import base_request
from checks import assert_status, assert_error
from models import Order

NO_ORDER = 9999  


@allure.feature("Store")
@allure.story("POST /store/order - создание заказа")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Позитивный: создание заказа")
def test_post_order(test_order):
    response = base_request.post("store/order", test_order.model_dump())
    assert_status(response, 200)
    assert Order(**response.json()).id == test_order.id
    base_request.delete("store/order", test_order.id)


@allure.feature("Store")
@allure.story("POST /store/order - создание заказа")
@allure.severity(allure.severity_level.MINOR)
@allure.title("Негативный: создание заказа с неверным телом")
def test_post_order_negative():
    response = base_request.post("store/order", {"id": "не число", "quantity": "много"})
    assert_error(response, (400, 405, 500))


@allure.feature("Store")
@allure.story("GET /store/order/{orderId} - получение заказа")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Позитивный: получение заказа по id")
def test_get_order(created_order):
    response = base_request.get("store/order", created_order.id)
    assert_status(response, 200)
    order = Order(**response.json())
    assert order.petId == created_order.petId
    assert order.quantity == created_order.quantity


@allure.feature("Store")
@allure.story("GET /store/order/{orderId} - получение заказа")
@allure.severity(allure.severity_level.MINOR)
@allure.title("Негативный: получение несуществующего заказа")
def test_get_order_negative():
    response = base_request.get("store/order", NO_ORDER, expected_status=404)
    assert_status(response, 404)


@allure.feature("Store")
@allure.story("GET /store/inventory - остатки питомцев")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Позитивный: получение остатков по статусам")
def test_get_inventory():
    response = base_request.get("store/inventory")
    assert_status(response, 200)
    assert isinstance(response.json(), dict)
    assert len(response.json()) > 0


@allure.feature("Store")
@allure.story("GET /store/inventory - остатки питомцев")
@allure.severity(allure.severity_level.MINOR)
@allure.title("Негативный: запрос с неподдерживаемым методом POST")
def test_get_inventory_negative():
    response = base_request.post("store/inventory")
    assert_error(response, (404, 405))


@allure.feature("Store")
@allure.story("DELETE /store/order/{orderId} - удаление заказа")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Позитивный: удаление заказа")
def test_delete_order(created_order):
    response = base_request.delete("store/order", created_order.id)
    assert_status(response, 200)
    get_response = base_request.get("store/order", created_order.id, expected_status=404)
    assert_status(get_response, 404)


@allure.feature("Store")
@allure.story("DELETE /store/order/{orderId} - удаление заказа")
@allure.severity(allure.severity_level.MINOR)
@allure.title("Негативный: удаление несуществующего заказа")
def test_delete_order_negative():
    response = base_request.delete("store/order", NO_ORDER)
    assert_status(response, 404)
