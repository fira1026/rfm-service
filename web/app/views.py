import requests
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from .forms import UploadFileForm

# Imaginary function to handle an uploaded file.
# from somewhere import handle_uploaded_file
from app.utils import handle_uploaded_file

# Create your views here.

@csrf_exempt
@api_view(['GET'])
def say_hello(request):
    return Response('Hello, World')

@api_view(['GET', 'POST'])
def upload_file(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # TODO: should do it in async task
            input_file_path = handle_uploaded_file(request.FILES["file"])

            # call api server to execute transfer_kaggle_data instead
            url = "http://localhost:8001/api/rfm-analysis"
            headers = {"Content-Type": "application/json"}
            data = {"file_path": input_file_path}
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                result_dict = response.json()
                return Response({"result file path": result_dict['file_path']})
            else:
                return Response({"message": f"Error: {response.status_code} - {response.text}"})

    else:
        form = UploadFileForm()
    return render(request, "upload.html", {"form": form})
