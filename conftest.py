import random
import pytest
from base_request import base_request
from models import Pet, Category, Tag, Order, User


@pytest.fixture
def test_pet():
    return Pet(id=random.randint(100000, 999999),
               category=Category(id=1, name="dogs"),
               name="Barsic",
               photoUrls=["string"],
               tags=[Tag(id=1, name="test")],
               status="available")


@pytest.fixture
def created_pet(test_pet):
    base_request.post("pet", test_pet.model_dump())
    base_request.get("pet", test_pet.id)          
    yield test_pet
    base_request.delete("pet", test_pet.id)       


@pytest.fixture
def test_order():
    return Order(id=random.randint(1, 10), petId=777, quantity=1,
                 shipDate="2026-10-15T10:00:00.000Z",
                 status="placed", complete=True)


@pytest.fixture
def created_order(test_order):
    base_request.post("store/order", test_order.model_dump())
    base_request.get("store/order", test_order.id)
    yield test_order
    base_request.delete("store/order", test_order.id)


def make_user():
    n = random.randint(100000, 999999)
    return User(id=n, username=f"user{n}", firstName="Andrew", lastName="S",
                email=f"user{n}@example.com", password="12345",
                phone="", userStatus=1)


@pytest.fixture
def test_user():
    return make_user()


@pytest.fixture
def created_user(test_user):
    base_request.post("user", test_user.model_dump())
    base_request.get("user", test_user.username)
    yield test_user
    base_request.delete("user", test_user.username)


@pytest.fixture
def test_users():
    return [make_user(), make_user()]
