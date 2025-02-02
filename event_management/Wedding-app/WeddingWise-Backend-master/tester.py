import requests

BASE_URL = "http://localhost:8888/api/auth"

# Login User
def login_user():
    endpoint = "/login-user"
    payload = {
        "email": "ronit.doe@example.com",
        "password": "securepassword123"
    }
    response = requests.post(BASE_URL + endpoint, json=payload)
    print("=== Login User ===")
    print("Status Code:", response.status_code)
    try:
        response_data = response.json()
        print("Response:", response_data)
        return response_data.get("token")  # Return JWT token
    except Exception as e:
        print("Error decoding response JSON:", e)
        print("Response Text:", response.text)
        return None


# Register Event
def register_event(token):
    endpoint = "/register-event"
    payload = {
        "date": "2025-03-01",
        "userId": "678f2df7581f718f4c87f642"  # Replace with actual user ID
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(BASE_URL + endpoint, json=payload, headers=headers)
    print("=== Register Event ===")
    print("Status Code:", response.status_code)
    try:
        print("Response:", response.json())
    except Exception as e:
        print("Error decoding response JSON:", e)
        print("Response Text:", response.text)


# Main Testing Workflow
if __name__ == "__main__":
    # Step 1: Log in the user and get the token
    token = login_user()
    print(token)
    if token:
        # Step 2: Register an event using the token
        register_event(token)
    else:
        print("Unable to register event as login failed.")
