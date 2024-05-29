import os
import zipfile
from io import BytesIO

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from typing import List

from tqdm import tqdm

from generate_description import WeatherDescriptionGenerator
from image_generation_api import ImageGenerator


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
async def root():
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


# @app.post("/generate-images/")
# async def generate_images(request: SentenceRequest):
#     try:
#         # Call the /generate-descriptions/ endpoint to get descriptions
#         descriptions_response = generate_descriptions(request)
#
#         # Extract descriptions
#         descriptions = descriptions_response.description_model
#
#         # Initialize the image generator
#         image_generator = ImageGenerator()
#
#         # Set content headers for streaming response
#         headers = {
#             "Content-Disposition": "attachment; filename=generated_images.zip",
#             "Content-Type": "application/zip",
#         }
#
#         # Generate images and stream them directly to the client
#         async def generate():
#             for idx, description in enumerate(descriptions):
#                 try:
#                     image = image_generator.generate_images(description.description)
#
#                     # Save the image to a BytesIO object
#                     img_byte_arr = BytesIO()
#                     image.save(img_byte_arr, format='PNG')
#                     img_byte_arr.seek(0)
#
#                     # Define the image filename
#                     image_filename = f"{description.location}_{description.weather_event}_{idx + 1}.png"
#
#                     # Read the image data from BytesIO
#                     img_data = img_byte_arr.getvalue()
#
#                     # Yield the image data to the client
#                     yield {
#                         "filename": image_filename,
#                         "image_data": img_data
#                     }
#
#                 except Exception as e:
#                     # Handle any exceptions during image generation
#                     raise HTTPException(status_code=500, detail=f"Error generating image: {str(e)}")
#
#         # Return the streaming response
#         return Response(generate(), headers=headers)
#
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")


@app.post("/generate-images/", response_model=List[str])
def generate_images(request: SentenceRequest):
    try:
        # Call the /generate-descriptions/ endpoint to get descriptions
        descriptions_response = generate_descriptions(request)

        # Extract descriptions
        descriptions = descriptions_response.description_model

        # Initialize the image generator
        image_generator = ImageGenerator()

        # Generate images
        # counter = 1
        # new_directory = f"{BASE_DIRECTORY}_{counter}"
        # while os.path.exists(new_directory):
        #     counter += 1
        #     new_directory = f"{BASE_DIRECTORY}_{counter}"
        # os.makedirs(new_directory)
        # print(f"Directory '{BASE_DIRECTORY}' already exists. Created '{new_directory}' instead.")

        images_data = []
        with tqdm(total=len(descriptions)) as pbar:
            for idx, description in enumerate(descriptions):
                image = image_generator.generate_images(description.description)
                filename = f"{description.location}_{description.weather_event}_{idx + 1}"
                # Save image with the formatted filename
                try:
                    image.save(f"generated_images_1/{filename}.png")  # Ensure the directory "images" exists
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Failed to save image: {str(e)}")

                # Save the image to a BytesIO object
                img_byte_arr = BytesIO()
                image.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()
                pbar.update(1)

                images_data.append((description.location, description.weather_event, img_byte_arr))

            # return all the images
            if images_data:
                # return Response(content=images_data, media_type="image/png")
                # location, weather_event, img_byte_arr = images_data[0]

                # Create a zip file containing all the images
                zip_file = BytesIO()
                with zipfile.ZipFile(zip_file, mode='w') as z:
                    for location, weather_event, img_byte_arr in images_data:
                        filename = f"{location}_{weather_event}_{idx+1}.png"
                        z.writestr(filename, img_byte_arr)
                zip_file.seek(0)
                return Response(content=zip_file.getvalue(), media_type="application/zip", headers={"Content-Disposition": "attachment; filename=generated_images.zip"})

                # return Response(content=img_byte_arr, media_type="image/png")
            else:
                raise HTTPException(status_code=500, detail="No images generated")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")


HOST = "http://127.0.0.1"
PORT = 8000
BASE_DIRECTORY = "generated_images"

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)

# @app.post("/generate-images/", response_model=List[str])
# def generate_images(request: SentenceRequest):
#     try:
#         @app.post("/generate-descriptions/", response_model=List[str])
#
#         image_generator = ImageGenerator()
#         images = image_generator.generate_images(request.sentence)
#         return images
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")


# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import List
# import requests
#
# from generate_description import WeatherDescriptionGenerator
# from image_generation_api import ImageGenerator
#
#
# class SentenceRequest(BaseModel):
#     sentence: str
#
#
# class Description(BaseModel):
#     description: str
#     location: str
#     weather_event: str
#
#
# class DescriptionsResponse(BaseModel):
#     descriptions: List[Description]
#
#
# class ImageRequest(BaseModel):
#     descriptions: List[Description]
#
#
# class ImagesResponse(BaseModel):
#     images: List[str]
#
#
# HOST = "http://127.0.0.1"
# PORT = 8000
#
# app = FastAPI()
#
#
# @app.get("/")
# async def root():
#     return {"message": "This is the root of the Text to Image Generation API"}
#
#
# @app.post("/generate-descriptions/", response_model=ImagesResponse)
# def generate_descriptions(request: SentenceRequest):
#     try:
#         # Generate descriptions
#         generator = WeatherDescriptionGenerator()
#         descriptions = generator.generate_descriptions(request.sentence)
#         detailed_descriptions = [{
#             "description": desc[0],
#             "location": desc[1],
#             "weather_event": desc[2]
#         } for desc in descriptions]
#
#         # Prepare payload for image generation
#         image_request_payload = {
#             "descriptions": detailed_descriptions
#         }
#
#         # Send POST request to generate images
#         response = requests.post(f"{HOST}:{PORT}/generate-images/", json=image_request_payload)
#
#         # Check for errors in the image generation response
#         if response.status_code != 200:
#             raise HTTPException(status_code=response.status_code, detail="Failed to generate images")
#
#         # Return images response
#         images_response = response.json()
#         return ImagesResponse(images=images_response["images"])
#
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
#
#
# @app.post("/generate-images/", response_model=ImagesResponse)
# def generate_images(request: ImageRequest):
#     try:
#         image_generator = ImageGenerator()
#         images = []
#         for description in request.descriptions:
#             image = image_generator.generate_images(description.description, description.location, description.weather_event)
#             images.append(image)
#         return ImagesResponse(images=images)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred while generating images: {str(e)}")
#
#
# # Run the FastAPI application
# if __name__ == "__main__":
#     import uvicorn
#
#     uvicorn.run(app, host=HOST, port=PORT)
