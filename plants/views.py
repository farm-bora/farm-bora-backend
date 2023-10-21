import uuid
import json
import base64
from rest_framework import generics, views
from rest_framework.response import Response
from gradio_client import Client
from pathlib import Path

from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from .models import Plant, Disease
from .serializers import (
    PlantSerializer,
    PlantDiseaseSearchSerializer,
    DiseaseSerializer,
    TTSSerializer,
)

import environ

# Initialise environment variables
environ.Env.read_env()

env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent


class PlantList(generics.ListAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer


class PlantDetail(generics.RetrieveAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer


class DiseaseList(generics.ListAPIView):
    serializer_class = DiseaseSerializer

    def get_queryset(self):
        return Disease.objects.filter(plant_id=self.kwargs.get("plant_id"))


class DiseaseDetail(generics.RetrieveAPIView):
    serializer_class = DiseaseSerializer

    def get_queryset(self):
        return Disease.objects.filter(plant_id=self.kwargs.get("plant_id"))


class PlantImageSearch(views.APIView):
    """Search for plant diseases"""

    serializer_class = PlantDiseaseSearchSerializer

    def post(self, request, format=None):
        serializer = PlantDiseaseSearchSerializer(data=request.data)
        if serializer.is_valid():
            image_base64 = serializer.data["image_base64"]
            # <actual-base64 string>
            encoded_image = image_base64.split(",")[1]

            header = image_base64.split(",")[0]  # data:image/png;base64
            header = header.split(":")[1]  # image/png;base64

            dtype = header.split(";")[0]  # image/png
            dtype = dtype.split("/")[1]  # png
            fpath = f"/tmp/{uuid.uuid4()}.{dtype}"
            with open(fpath, "wb") as f:
                f.write(base64.b64decode(encoded_image))

            try:
                ML_URL = env("ML_URL", default="http://localhost:7860/")
                client = Client(ML_URL)
                result = client.predict(fpath, api_name="/predict")
                with open(result[0], "r") as f:
                    result_json = f.read()

                result_dict = json.loads(result_json)
                result_dict["time"] = result[1]

                print(result_dict["confidences"])
                for i, prediction in enumerate(result_dict["confidences"]):
                    slug_label = prediction["label"].lower()
                    plant_label = slug_label.split("___")[0]
                    disease_label = slug_label.split("___")[1]

                    print(
                        f"[INFO] Searching Slug Label: {slug_label} Disease: {disease_label}"
                    )
                    if disease_label == "healthy":
                        plant = Plant.objects.get(slug=plant_label)

                        result_dict["confidences"][i]["diagnosis"] = "healthy"
                        result_dict["confidences"][i]["plant_id"] = plant.id
                        result_dict["confidences"][i]["plant_name"] = plant.name
                    else:
                        disease = Disease.objects.get(slug=slug_label)

                        print(f"Slug Label: {slug_label} : {disease.name} : ")
                        result_dict["confidences"][i]["diagnosis"] = "not healthy"
                        result_dict["confidences"][i]["disease_id"] = disease.id
                        result_dict["confidences"][i]["plant_id"] = disease.plant_id
                        result_dict["confidences"][i]["diagnosis"] = disease.name
                        result_dict["confidences"][i]["plant_name"] = disease.plant.name

                return Response(result_dict)
            except Exception as error:
                print(f"Exception {__name__}:: {error}")
                result_dict = {"message": "Could not reach AI Model"}
                return Response(result_dict, 503)
        else:
            return Response(serializer.errors, status=422)


class TextToSpeech(views.APIView):
    """Convert text to speech using IBM Watson TTS"""

    serializer_class = TTSSerializer

    def post(self, request, format=None):
        serializer = TTSSerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.data["text"]
            authenticator = IAMAuthenticator(env("tts_apikey"))
            text_to_speech = TextToSpeechV1(authenticator=authenticator)

            text_to_speech.set_service_url(env("tts_url"))
            fname = f"media/{uuid.uuid4()}.wav"
            with open(BASE_DIR / fname, "wb") as audio_file:
                audio_file.write(
                    text_to_speech.synthesize(
                        text, voice="en-US_AllisonV3Voice", accept="audio/wav"
                    )
                    .get_result()
                    .content
                )
                result_dict = {"path": fname}

            return Response(result_dict)
        else:
            return Response(serializer.errors, status=422)


#     curl -X POST -u "apikey:{apikey}" \
# --header "Content-Type: application/json" \
# --header "Accept: audio/wav" \
# --data "{\"text\":\"hello world\"}" \
# --output hello_world.wav \
# "{url}/v1/synthesize?voice=en-US_MichaelV3Voice"
#
