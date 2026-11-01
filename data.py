class Message:
    USER_EXISTS = {
        "success": False,
        "message": "User already exists"
    }

    MISSING_FIELDS = {
        "success": False,
        "message": "Email, password and name are required fields"
    }

    LOGIN_FAILED = {
        "success": False,
        "message": "email or password are incorrect"
    }

    UNAUTHORIZED = {
        "success": False,
        "message": "You should be authorised"
    }

    NO_INGREDIENTS = {
        "success": False,
        "message": "Ingredient ids must be provided"
    }


class TestData:
    NONEXISTENT_EMAIL = 'unknown_login_123_avadakedavra'
    NONEXISTENT_PASSWORD = 'unknown_password_123_avadakedavra'
    INVALID_INGREDIENT_HASH = ["invalid-hash-123-avadakedavra"]