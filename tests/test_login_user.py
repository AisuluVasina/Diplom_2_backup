import pytest
import allure
from api_client import ApiClient
from data import Message

@allure.feature('Авторизация пользователя')
class TestLoginUser:
    
    @allure.title('Успешная авторизация существующего пользователя')
    def test_login_success(self, registered_user):
        with allure.step("Выполняем авторизацию"):
            response = ApiClient.login_user(
                registered_user["email"], 
                registered_user["password"]
            )
            
        with allure.step("Проверяем успешный ответ"):
            assert response.status_code == 200
            assert response.json()["success"] is True
            assert response.json()["user"]["email"] == registered_user["email"]
    
    @allure.title('Неудачная авторизация с неверным email')
    def test_login_invalid_email(self, registered_user):
        with allure.step("Пытаемся авторизоваться с неверным email"):
            response = ApiClient.login_user(
                "invalid-email@example.com", 
                registered_user["password"]
            )
            
        with allure.step("Проверяем ошибку авторизации"):
            assert response.status_code == 401
            assert response.json() == Message.LOGIN_FAILED
    
    @allure.title('Неудачная авторизация с неверным паролем')
    def test_login_invalid_password(self, registered_user):
        with allure.step("Пытаемся авторизоваться с неверным паролем"):
            response = ApiClient.login_user(
                registered_user["email"], 
                "wrong-password123"
            )
            
        with allure.step("Проверяем ошибку авторизации"):
            assert response.status_code == 401
            assert response.json() == Message.LOGIN_FAILED