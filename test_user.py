import time
import allure
from base_request import base_request
from checks import assert_status, assert_error
from models import User

NO_USER = "no_such_user_xyz"


@allure.feature("User")
@allure.story("POST /user - создание пользователя")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Позитивный: создание пользователя")
def test_post_user(test_user):
    response = base_request.post("user", test_user.model_dump())
    assert_status(response, 200)
    base_request.delete("user", test_user.username)


@allure.feature("User")
@allure.story("POST /user - создание пользователя")
@allure.severity(allure.severity_level.MINOR)
@allure.title("Негативный: создание пользователя с неверным телом")
def test_post_user_negative():
    response = base_request.post("user", {"id": "не число", "userStatus": "статус"})
    assert_error(response, (400, 405, 500))


@allure.feature("User")
@allure.story("GET /user/{username} - получение пользователя")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Позитивный: получение пользователя по имени")
def test_get_user(created_user):
    response = base_request.get("user", created_user.username)
    assert_status(response, 200)
    user = User(**response.json())
    assert user.username == created_user.username
    assert user.email == created_user.email


@allure.feature("User")
@allure.story("GET /user/{username} - получение пользователя")
@allure.severity(allure.severity_level.MINOR)
@allure.title("Негативный: получение несуществующего пользователя")
def test_get_user_negative():
    response = base_request.get("user", NO_USER, expected_status=404)
    assert_status(response, 404)


@allure.feature("User")
@allure.story("PUT /user/{username} - обновление пользователя")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Позитивный: обновление имени пользователя")
def test_put_user(created_user):
    updated = created_user.model_copy(update={"firstName": "Maomao"})
    response = base_request.put("user", updated.model_dump(), endpoint_id=created_user.username)
    assert_status(response, 200)
    time.sleep(2)
    get_response = base_request.get("user", created_user.username)
    assert User(**get_response.json()).firstName == "Maomao"


@allure.feature("User")
@allure.story("PUT /user/{username} - обновление пользователя")
@allure.severity(allure.severity_level.MINOR)
@allure.title("Негативный: обновление с неверным телом")
def test_put_user_negative():
    response = base_request.put("user", {"id": "не число"}, endpoint_id=NO_USER)
    assert_error(response, (400, 404, 405, 500))


@allure.feature("User")
@allure.story("DELETE /user/{username} - удаление пользователя")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Позитивный: удаление пользователя")
def test_delete_user(created_user):
    response = base_request.delete("user", created_user.username)
    assert_status(response, 200)
    get_response = base_request.get("user", created_user.username, expected_status=404)
    assert_status(get_response, 404)


@allure.feature("User")
@allure.story("DELETE /user/{username} - удаление пользователя")
@allure.severity(allure.severity_level.MINOR)
@allure.title("Негативный: удаление несуществующего пользователя")
def test_delete_user_negative():
    response = base_request.delete("user", NO_USER)
    assert_status(response, 404)


@allure.feature("User")
@allure.story("GET /user/login - вход в систему")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Позитивный: вход пользователя")
def test_login(created_user):
    response = base_request.get("user/login",
                                params={"username": created_user.username,
                                        "password": created_user.password})
    assert_status(response, 200)
    assert "logged in" in response.json()["message"]


@allure.feature("User")
@allure.story("GET /user/login - вход в систему")
@allure.severity(allure.severity_level.MINOR)
@allure.title("Негативный: вход методом POST (метод не поддерживается)")
def test_login_negative():
    response = base_request.post("user/login")
    assert_error(response, (404, 405))


@allure.feature("User")
@allure.story("GET /user/logout - выход из системы")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Позитивный: выход пользователя")
def test_logout():
    response = base_request.get("user/logout")
    assert_status(response, 200)


@allure.feature("User")
@allure.story("GET /user/logout - выход из системы")
@allure.severity(allure.severity_level.MINOR)
@allure.title("Негативный: выход методом POST (метод не поддерживается)")
def test_logout_negative():
    response = base_request.post("user/logout")
    assert_error(response, (404, 405))


@allure.feature("User")
@allure.story("POST /user/createWithList - создание списка пользователей")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Позитивный: создание двух пользователей списком")
def test_create_with_list(test_users):
    response = base_request.post("user/createWithList", [u.model_dump() for u in test_users])
    assert_status(response, 200)
    for u in test_users:
        base_request.delete("user", u.username)


@allure.feature("User")
@allure.story("POST /user/createWithList - создание списка пользователей")
@allure.severity(allure.severity_level.MINOR)
@allure.title("Негативный: вместо списка передан объект")
def test_create_with_list_negative():
    response = base_request.post("user/createWithList", {"username": 123})
    assert_error(response, (400, 405, 500))


@allure.feature("User")
@allure.story("POST /user/createWithArray - создание массива пользователей")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Позитивный: создание двух пользователей массивом")
def test_create_with_array(test_users):
    response = base_request.post("user/createWithArray", [u.model_dump() for u in test_users])
    assert_status(response, 200)
    for u in test_users:
        base_request.delete("user", u.username)


@allure.feature("User")
@allure.story("POST /user/createWithArray - создание массива пользователей")
@allure.severity(allure.severity_level.MINOR)
@allure.title("Негативный: вместо массива передан объект")
def test_create_with_array_negative():
    response = base_request.post("user/createWithArray", {"username": 123})
    assert_error(response, (400, 405, 500))
