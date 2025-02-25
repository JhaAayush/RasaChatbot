import requests

# Define the Rasa server URL
url = "http://localhost:5005/webhooks/rest/webhook"

# Define the payload (user message)
payload = {
    "sender": "user123",  # Unique ID for the user
    "message": "I am interested in marketing. Suggest electives."    # User message
}

try:
    # Send the POST request
    response = requests.post(url, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        print("Bot's response:", response.json())
        bot_response = response.json()
        print(bot_response["text"])
    else:
        print(f"Failed to get a response. Status code: {response.status_code}")
        print("Response text:", response.text)
except requests.exceptions.ConnectionError as e:
    print("Connection error: The Rasa server is not running or is unreachable.")
    print("Make sure the Rasa server is running on http://localhost:5005.")
except Exception as e:
    print("An unexpected error occurred:", str(e))