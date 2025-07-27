import pytest
from my_app.main import get_user_data
import requests

# Имитация API, если нет реального
# Если есть реальный тестовый API, используй его URL
MOCKED_API_URL = "http://mockapi.example.com/users/"

def test_get_existing_user():
    # Если нет реального API, можно протестировать внутреннюю функцию
    user = get_user_data(1)
    assert user is not None
    assert user["name"] == "Test User"

def test_get_non_existing_user():
    # Если нет реального API
    user = get_user_data(99)
    assert user is None

# Пример теста, который требовал бы реального API
# def test_real_api_user_endpoint():
#     response = requests.get(f"{MOCKED_API_URL}1")
#     assert response.status_code == 200
#     assert response.json()["name"] == "Test User"

# 12. HTTPS request of an open button is 200
def test_HTTPS_request_of_open_button_is_200():
    response = requests.get('https://qaplayground.dev/apps/popup/')

    assert response.status_code == 200  

# 13. HTTPS request of a submit button is 200
def test_HTTPS_request_of_submit_button_is_200():
    response = requests.get('https://qaplayground.dev/apps/popup/popup')

    assert response.status_code == 200
