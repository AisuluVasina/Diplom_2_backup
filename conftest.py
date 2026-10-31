import pytest
from api_client import ApiClient
from generators import generate_user_data

# Вспомогательные функции (НЕ фикстуры)
def _register_user(user_data):
    """Регистрирует пользователя через основной клиент API"""
    response = ApiClient.register_user(user_data)
    if response.status_code != 200:
        raise RuntimeError(f"Не удалось зарегистрировать пользователя: {response.text}")
    return user_data

def _login_and_get_token(user_data):
    """Логинит пользователя и возвращает токен"""
    response = ApiClient.login_user(user_data["email"], user_data["password"])
    if response.status_code != 200:
        raise RuntimeError(f"Не удалось авторизоваться: {response.text}")
    return response.json()["accessToken"]

@pytest.fixture(scope="function")
def order_context():
    """
    Фикстура для тестов создания заказа.
    Подготавливает: токен, ID ингредиента.
    """
    user_data = generate_user_data()
    
    # Используем общую функцию регистрации (через ApiClient)
    _register_user(user_data)
    
    # Получаем токен
    access_token = _login_and_get_token(user_data)

    # Получаем ингредиенты
    ingredients_resp = ApiClient.get_ingredients()
    if ingredients_resp.status_code != 200:
        raise RuntimeError(f"Не удалось получить ингредиенты: {ingredients_resp.text}")
    
    ingredients_list = ingredients_resp.json().get('data', )
    if not ingredients_list:
        raise ValueError("Список ингредиентов пуст!")
    
    valid_ingredient_id = ingredients_list[0]["_id"]

    yield {
        "token": access_token,
        "ingredient_id": valid_ingredient_id
    }

    # Очистка: удаляем пользователя через новый метод ApiClient
    try:
        ApiClient.delete_user(access_token)
    except Exception:
        pass

@pytest.fixture(scope="function")
def registered_user():
    """
    Фикстура для тестов, где нужен просто существующий пользователь.
    Возвращает данные пользователя (email, password, name).
    """
    user_data = generate_user_data()
    
    # Используем общую функцию регистрации
    _register_user(user_data)

    yield user_data

    # Очистка
    try:
        access_token = _login_and_get_token(user_data)
        ApiClient.delete_user(access_token)
    except RuntimeError:
        pass

@pytest.fixture(scope="function")
def cleanup_user(request):
    """
    ФИКСТУРА ДЛЯ ОЧИСТКИ.
    Не создает пользователя. Принимает данные пользователя через yield.
    Удаляет пользователя после теста.
    """
    yield  # Здесь выполняется тест
    user_data = getattr(request.cls, "user_to_cleanup", None)
    
    # Блок очистки (выполняется всегда после теста)
    if user_data:
        try:
            access_token = _login_and_get_token(user_data)
            ApiClient.delete_user(access_token)
            request.cls.user_to_cleanup = None 
        except Exception as e:
            # Игнорируем ошибки очистки, чтобы не маскировать ошибку самого теста
            pass