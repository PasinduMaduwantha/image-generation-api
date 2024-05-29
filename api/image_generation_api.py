import io

import requests
from PIL import Image
from fastapi import HTTPException


class ImageGenerator:
    def __init__(self):
        self.API_URL = "https://oqcfgs6w2huz6cyb.us-east-1.aws.endpoints.huggingface.cloud"
        self.headers = {
            "Accept": "image/png",
            "Authorization": "Bearer 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",
            "Content-Type": "application/json"
        }
        # self.generator = WeatherDescriptionGenerator()


    def query(self, payload):
        response = requests.post(self.API_URL, headers=self.headers, json=payload)
        if response.status_code == 200:
            return response.content
        else:
            response.raise_for_status()

    def generate_images(self, description):

        try:
            output = self.query({
                "inputs": description,
                "parameters": {
                    "negative_prompt": "ugly, blurred, distorted"
                }
            })
            image = Image.open(io.BytesIO(output))
            return image
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")

