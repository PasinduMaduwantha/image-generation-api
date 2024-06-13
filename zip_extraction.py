import requests
import zipfile
import io
import os

# Define your FastAPI endpoint URL
API_URL = 'http://localhost:8000/generate-images/'  # Replace with your actual API URL
BASE_DIRECTORY = "generated_images"
# Define the request body
request_body = {
  "sentence": "rain_jaffna"
}


def request_images_and_save():
    try:
        # Send a POST request to the endpoint with the request body
        response = requests.post(API_URL, json=request_body)

        # Check if the request was successful
        if response.status_code == 200:
            # Save the received zip file
            with open('generated_images.zip', 'wb') as f:
                f.write(response.content)
            print('Zip file saved successfully.')

            #save the zip file in the directory
            # with open(f'{BASE_DIRECTORY}.zip', 'wb') as f:
            #     f.write(response.content)

            # Extract images from the zip file
            extract_images_from_zip()

        else:
            print(f'Request failed with status code {response.status_code}: {response.text}')

    except requests.RequestException as e:
        print(f'Error sending request: {str(e)}')


def extract_images_from_zip():
    try:
        counter = 1
        new_directory = f"{BASE_DIRECTORY}_{counter}"
        while os.path.exists(new_directory):
            counter += 1
            new_directory = f"{BASE_DIRECTORY}_{counter}"
        os.makedirs(new_directory)
        print(f"Directory '{BASE_DIRECTORY}' already exists. Created '{new_directory}' instead.")
        # Create a directory for extracted images
        extracted_images_dir = new_directory
        if not os.path.exists(extracted_images_dir):
            os.makedirs(extracted_images_dir)

        # Open the saved zip file
        with zipfile.ZipFile('generated_images.zip', 'r') as zip_ref:
            # Extract all contents
            zip_ref.extractall(extracted_images_dir)
        print(f'Images extracted successfully to {extracted_images_dir}.')

    except zipfile.BadZipFile as e:
        print(f'Error extracting zip file: {str(e)}')


if __name__ == '__main__':
    request_images_and_save()
