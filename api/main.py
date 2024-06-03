import os
import zipfile
from io import BytesIO
import uvicorn
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from typing import List

from tqdm import tqdm

from api.generate_description import WeatherDescriptionGenerator
from api.image_generation_api import ImageGenerator


class SentenceRequest(BaseModel):
    sentence: str


class Description(BaseModel):
    description: str
    location: str
    weather_event: str


class DetailedDescriptionsResponse(BaseModel):
    description_model: List[Description]


app = FastAPI()


@app.get("/")
def root():
    return {"message": "This is the root of the Text to Image Generation API"}


@app.post("/generate-descriptions/", response_model=DetailedDescriptionsResponse)
def generate_descriptions(request: SentenceRequest):
    try:
        generator = WeatherDescriptionGenerator()
        descriptions = generator.generate_descriptions(request.sentence)
        detailed_descriptions = [{
            "description": str(desc[0]),
            "location": str(desc[1]),
            "weather_event": str(desc[2])
        } for desc in descriptions]
        return DetailedDescriptionsResponse(description_model=detailed_descriptions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Description generation failed: {str(e)}")

@app.post("/generate-images/", response_model=List[str])
def generate_images(request: SentenceRequest):
    try:
        # Call the /generate-descriptions/ endpoint to get descriptions
        descriptions_response = generate_descriptions(request)

        # Extract descriptions
        descriptions = descriptions_response.description_model

        # Initialize the image generator
        image_generator = ImageGenerator()
        images_data = []
        with tqdm(total=len(descriptions)) as pbar:
            for idx, description in enumerate(descriptions):
                image = image_generator.generate_images(description.description)

                # Save the image to a BytesIO object
                img_byte_arr = BytesIO()
                image.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()
                pbar.update(1)

                images_data.append((description.location, description.weather_event, img_byte_arr))

            # return all the images
            if images_data:

                # Create a zip file containing all the images
                zip_file = BytesIO()
                img_id_counter = 1
                with zipfile.ZipFile(zip_file, mode='w') as z:
                    for location, weather_event, img_byte_arr in images_data:
                        filename = f"{img_id_counter}_{location}_{weather_event}.png"
                        z.writestr(filename, img_byte_arr)
                        img_id_counter += 1
                zip_file.seek(0)
                return Response(content=zip_file.getvalue(), media_type="application/zip", headers={"Content-Disposition": "attachment; filename=generated_images.zip"})

                # return Response(content=img_byte_arr, media_type="image/png")
            else:
                raise HTTPException(status_code=500, detail="No images generated")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")


BASE_DIRECTORY = "generated_images"

HOST = "http://localhost"

# Run the FastAPI application
if __name__ == "__main__":

    uvicorn.run(app, host=HOST, port=8000)

