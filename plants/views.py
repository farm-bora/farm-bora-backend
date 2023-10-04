from rest_framework import generics, views
from rest_framework.response import Response
import base64
import uuid
import json
from gradio_client import Client

from .models import Plant
from .serializers import PlantSerializer, PlantDiseaseSearchSerializer


class PlantList(generics.ListAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer


class PlantDetail(generics.RetrieveAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer


class PlantImageSearch(views.APIView):
    """Search for plant diseases"""

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

            client = Client("http://localhost:7860/")
            result = client.predict(fpath, api_name="/predict")
            with open(result[0], "r") as f:
                result_json = f.read()

            result_dict = json.loads(result_json)
            result_dict["time"] = result[1]
            print(result_dict)

            return Response(result_dict)
        else:
            return Response(serializer.errors, status=422)
