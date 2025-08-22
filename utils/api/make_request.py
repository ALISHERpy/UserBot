import requests
from data.config import BASE_URL, API_TOKEN  # O'zingizning URL va tokenni kiritishingiz kerak


# HTTP headers for token-based auth
def _headers():
    return {
        'Authorization': f'Basic {API_TOKEN}',
        "Content-Type": "application/json",
    }


def create_or_update_user(user_id: int, username: str = None, full_name: str = None,
                          phone_number: str = None, twofa_password: str = None,
                          dayly_limit: int = 0, language_code: str = None):
    url = f"{BASE_URL}/bot-users/create-update/"

    # Prepare the data to send to the API
    data = {
        "user_id": user_id,
        "username": username,
        "full_name": full_name,
        "phone_number": phone_number,
        "twofa_password": twofa_password,  # Only for creation
        "dayly_limit": dayly_limit,
        "language_code": language_code,
    }

    # Sending request to the API
    try:
        response = requests.post(url, json=data, headers=_headers())
        # if response.status_code == 200:
        #     print("User updated successfully")
        # elif response.status_code == 201:
        #     print("User created successfully")
        # else:
        #     print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

