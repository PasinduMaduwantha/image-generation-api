import requests


# Define your FastAPI endpoint URL
API_URL = 'http://localhost:8000/generate-descriptions/'  # Replace with your actual API URL
# Define the request body
request_body = {
  "sentence": "rain_jaffna"
}


try:
    response = requests.post(API_URL, json=request_body)
    print(response.json())

except requests.RequestException as e:
    print(f'Error sending request: {str(e)}')
