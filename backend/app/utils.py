from app.core.config import AvailableServices
from huggingface_hub import InferenceClient
import base64
from io import BytesIO
from fastapi import HTTPException

class ServicesRunner:
    def __init__(self):
        pass
    def hugging_face_runner(self,input_prompt,service_name):
        try:
            client = None
            if service_name == "fal-ai" or service_name == "replicate" or service_name == "hf":
                if service_name == "fal-ai":
                    client = InferenceClient(token=AvailableServices.FAL_TOKEN)

                elif service_name == "replicate":
                    client = InferenceClient(token=AvailableServices.REPLICATE_TOKEN.value)
                    # print("REPLICATE_TOKEN: ",AvailableServices.REPLICATE_TOKEN.value)
                elif service_name == "hf":
                    client = InferenceClient(token=AvailableServices.HF_TOKEN.value)
                    # print("HF_TOKEN: ",AvailableServices.HF_TOKEN.value)

                image = client.text_to_image(
                    prompt=input_prompt,
                    model="stabilityai/stable-diffusion-3.5-large"
                )
                buffered = BytesIO()
                image.save(buffered, format="PNG")
                image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
                return {
                    "message": "Image generated successfully!",
                    "image_base64": image_base64
                }
            else:
                raise HTTPException(status_code=400, detail="Invalid service name") # Invalid service name  

        except Exception as e:
            print("ERROR IN THE SERIVICE hugging-runner FUNCITON: ",str(e))
            raise HTTPException(status_code=500, detail="ERROR IN THE SERIVICE FUNCITON")

    def run(self, service_name, input_prompt):
        pass


