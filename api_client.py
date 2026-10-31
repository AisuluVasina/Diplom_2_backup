import requests
import allure 
from urls import URL

class ApiClient:
    
    @staticmethod
    @allure.step("Регистрация пользователя")
    def register_user(data):
        return requests.post(URL.REGISTER_USER_URL, json=data)
    
    @staticmethod
    @allure.step("Авторизация пользователя")
    def login_user(email, password):
        return requests.post(URL.LOGIN_USER_URL, json={"email": email, "password": password})
    
    @staticmethod
    @allure.step("Создание заказа")
    def create_order(ingredients, token=None):
        headers = {"Authorization": f"{token}"} if token else {}
        return requests.post(URL.ORDERS_URL, json={"ingredients": ingredients}, headers=headers)

    @staticmethod
    @allure.step("Получить список ингредиентов")
    def get_ingredients():
        return requests.get(URL.INGREDIENTS_URL)

    @staticmethod
    @allure.step("Удаление пользователя")
    def delete_user(token):
        headers = {"Authorization": f"Bearer {token}"}
        return requests.delete(URL.REGISTER_USER_URL, headers=headers)