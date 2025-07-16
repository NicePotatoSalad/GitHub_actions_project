def get_app_version():
    return "1.0.0"

def get_user_data(user_id):
    if user_id == 1:
        return {"id": 1, "name": "Test User"}
    return None

def check_landing_page_title():
    return "Welcome to Our Public Landing Page!"