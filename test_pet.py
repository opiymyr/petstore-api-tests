import time
import allure
from pydantic import ValidationError
import pytest
from base_request import base_request
from checks import assert_status, assert_error
from models import Pet

NO_PET = -1  


@allure.feature("Pet")
@allure.story("POST /pet - создание питомца")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Позитивный: создание питомца")
def test_post_pet(test_pet):
    response = base_request.post("pet", test_pet.model_dump())
    assert_status(response, 200)
    assert Pet(**response.json()).name == test_pet.name
    base_request.delete("pet", test_pet.id)


@allure.feature("Pet")
@allure.story("POST /pet - создание питомца")
@allure.severity(allure.severity_level.MINOR)
@allure.title("Негативный: создание питомца с неверным телом")
def test_post_pet_negative():
    response = base_request.post("pet", {"id": "не число", "name": 123})
    assert_error(response, (400, 405, 500))


@allure.feature("Pet")
@allure.story("GET /pet/{petId} - получение питомца")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Позитивный: получение питомца по id")
def test_get_pet(created_pet):
    response = base_request.get("pet", created_pet.id)
    assert_status(response, 200)
    pet = Pet(**response.json())
    assert pet.id == created_pet.id
    assert pet.name == created_pet.name


@allure.feature("Pet")
@allure.story("GET /pet/{petId} - получение питомца")
@allure.severity(allure.severity_level.MINOR)
@allure.title("Негативный: получение несуществующего питомца")
def test_get_pet_negative():
    response = base_request.get("pet", NO_PET, expected_status=404)
    assert_status(response, 404)


@allure.feature("Pet")
@allure.story("PUT /pet - обновление питомца")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Позитивный: обновление имени и статуса")
def test_put_pet(created_pet):
    updated = created_pet.model_copy(update={"name": "Murzik", "status": "sold"})
    response = base_request.put("pet", updated.model_dump())
    assert_status(response, 200)
    time.sleep(2) 
    get_response = base_request.get("pet", created_pet.id)
    pet = Pet(**get_response.json())
    assert pet.name == "Murzik"
    assert pet.status == "sold"


@allure.feature("Pet")
@allure.story("PUT /pet - обновление питомца")
@allure.severity(allure.severity_level.MINOR)
@allure.title("Негативный: обновление с неверным телом")
def test_put_pet_negative():
    response = base_request.put("pet", {"id": "не число"})
    assert_error(response, (400, 405, 500))


@allure.feature("Pet")
@allure.story("DELETE /pet/{petId} - удаление питомца")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Позитивный: удаление питомца")
def test_delete_pet(created_pet):
    response = base_request.delete("pet", created_pet.id)
    assert_status(response, 200)
    get_response = base_request.get("pet", created_pet.id, expected_status=404)
    assert_status(get_response, 404)


@allure.feature("Pet")
@allure.story("DELETE /pet/{petId} - удаление питомца")
@allure.severity(allure.severity_level.MINOR)
@allure.title("Негативный: удаление несуществующего питомца")
def test_delete_pet_negative():
    response = base_request.delete("pet", NO_PET)
    assert_status(response, 404)


@allure.feature("Pet")
@allure.story("GET /pet/findByStatus - поиск по статусу")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Позитивный: поиск питомцев со статусом available")
def test_find_by_status():
    response = base_request.get("pet/findByStatus", params={"status": "available"})
    assert_status(response, 200)
    pets = response.json()
    assert isinstance(pets, list) and len(pets) > 0
    assert all(p.get("status") == "available" for p in pets)


@allure.feature("Pet")
@allure.story("GET /pet/findByStatus - поиск по статусу")
@allure.severity(allure.severity_level.MINOR)
@allure.title("Негативный: поиск по несуществующему статусу")
def test_find_by_status_negative():
    response = base_request.get("pet/findByStatus", params={"status": "unknown"},
                                expected_status=400)
    assert response.status_code == 400 or response.json() == []


@allure.feature("Pet")
@allure.story("GET /pet/findByTags - поиск по тегам")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Позитивный: поиск питомцев по тегу")
def test_find_by_tags():
    response = base_request.get("pet/findByTags", params={"tags": "test"})
    assert_status(response, 200)
    assert isinstance(response.json(), list)


@allure.feature("Pet")
@allure.story("GET /pet/findByTags - поиск по тегам")
@allure.severity(allure.severity_level.MINOR)
@allure.title("Негативный: поиск по несуществующему тегу")
def test_find_by_tags_negative():
    response = base_request.get("pet/findByTags", params={"tags": "no_such_tag_xyz"})
    assert response.status_code == 400 or response.json() == []


@allure.feature("Pet")
@allure.story("POST /pet/{petId} - обновление через форму")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Позитивный: обновление имени и статуса через форму")
def test_update_pet_form(created_pet):
    response = base_request.post("pet", endpoint_id=created_pet.id,
                                 data={"name": "Rex", "status": "sold"})
    assert_status(response, 200)
    time.sleep(2)
    get_response = base_request.get("pet", created_pet.id)
    assert Pet(**get_response.json()).name == "Rex"


@allure.feature("Pet")
@allure.story("POST /pet/{petId} - обновление через форму")
@allure.severity(allure.severity_level.MINOR)
@allure.title("Негативный: обновление через форму несуществующего питомца")
def test_update_pet_form_negative():
    response = base_request.post("pet", endpoint_id=NO_PET, data={"name": "Rex"})
    assert_error(response, (400, 404, 405))


@allure.feature("Pet")
@allure.story("POST /pet/{petId}/uploadImage - загрузка картинки")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Позитивный: загрузка файла для питомца")
def test_upload_image(created_pet):
    files = {"file": ("test.txt", b"hello petstore", "text/plain")}
    response = base_request.post("pet", endpoint_id=f"{created_pet.id}/uploadImage",
                                 data={"additionalMetadata": "test"}, files=files)
    assert_status(response, 200)
    assert "File uploaded" in response.json()["message"]


@allure.feature("Pet")
@allure.story("POST /pet/{petId}/uploadImage - загрузка картинки")
@allure.severity(allure.severity_level.MINOR)
@allure.title("Негативный: загрузка файла по неверному id")
def test_upload_image_negative():
    files = {"file": ("test.txt", b"hello", "text/plain")}
    response = base_request.post("pet", endpoint_id="abc/uploadImage", files=files)
    assert_error(response, (400, 404, 405, 500))


@allure.feature("Pet")
@allure.story("Валидация модели Pydantic")
@allure.severity(allure.severity_level.MINOR)
@allure.title("Pydantic отклоняет неверные данные")
def test_pydantic_invalid():
    with pytest.raises(ValidationError):
        Pet(id="не число", name="X", photoUrls=["a"], status="неизвестный")
