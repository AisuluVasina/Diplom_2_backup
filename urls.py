class URL:
    BASE_URL = 'https://qa-stellarburgers.education-services.ru'

    # Пользователь: регистрация и авторизация
    REGISTER_USER_URL = f'{BASE_URL}/api/auth/register' # POST - создание пользователя
    LOGIN_USER_URL = f'{BASE_URL}/api/auth/login'  # POST - авторизация пользователя

    # Ингредиенты и заказы
    ORDERS_URL = f'{BASE_URL}/api/orders'
    INGREDIENTS_URL = f'{BASE_URL}/api/ingredients'