import requests


# Define your FastAPI endpoint URL
API_URL = 'http://localhost:8000/generate-descriptions/'  # Replace with your actual API URL
# Define the request body
request_body = {
  "sentence": "There will be several rainy seasons in Eastern and Uva provinces and Polonnaruwa, Matale and Nuwara Eliya districts."
              " Light rain may occur in Northern Province and Anuradhapura district. Rain or thundershowers may occur at a few places in Western and Sabaragamuwa provinces and Galle and Matara districts after around 2.00 pm. Moderate gusty winds of around 30-40 kmph can be expected at times in Central, Uva and Eastern Provinces. Foggy conditions can be expected in Western and Sabaragamuwa provinces and Galle and Matara districts in the morning."
}


try:
    response = requests.post(API_URL, json=request_body)
    print(response.json())

except requests.RequestException as e:
    print(f'Error sending request: {str(e)}')
