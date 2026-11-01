import pytest
import allure
from generators import generate_user_data
from api_client import ApiClient
from data import TestData

@allure.feature('Создание заказа')
class TestCreateOrder:

    @allure.title('Успешное создание заказа с авторизацией и ингредиентами')
    def test_create_order_with_auth_and_ingredients(self, order_context):
        token = order_context["token"]
        ingredient_id = order_context["ingredient_id"]
        
        response = ApiClient.create_order([ingredient_id], token)
        assert response.status_code == 200
        resp_json = response.json()
        assert resp_json.get('success') is True
        assert 'order' in resp_json and 'number' in resp_json['order']

    @allure.title('Создание заказа без авторизации')
    def test_create_order_without_auth(self, order_context):
        ingredient_id = order_context["ingredient_id"]
        response = ApiClient.create_order([ingredient_id], "")
        assert response.status_code == 200

    @allure.title('Создание заказа без ингредиентов')
    def test_create_order_without_ingredients(self, order_context):
        token = order_context["token"]
        response = ApiClient.create_order([], token)
        assert response.status_code == 400

    @allure.title('Создание заказа с неверным хешем ингредиентов')
    def test_create_order_with_invalid_ingredient_hash(self, order_context):
        token = order_context["token"]
        response = ApiClient.create_order([TestData.INVALID_INGREDIENT_HASH], token)
        assert response.status_code == 500