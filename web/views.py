from django.shortcuts import render

from django.views import View
from django.template import loader
from django.conf import settings
from .forms import MyForm
import numpy as np
import cv2
import requests as req
from PIL import Image
import keras
import csv

def load_csv_file():
  classes = {}
  with open('D:\\Fils 4th year\\Licenta\\anaconda\\dataset\\labels.csv', 'r') as file:
      reader = csv.reader(file)
      for row in reader:
        try:
          classes[int(row[0])] = row[1]
        except:
          pass
      return classes

def grayscale(img):
    img = cv2.bitwise_not(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
    return img

def equalizeLighting(img):
    img = cv2.equalizeHist(img)
    return img

def preprocessing(img):
    img = grayscale(img)
    img = equalizeLighting(img)
    img = img / 255
    return img

class FormView(View):

    def get(self, request):
        template = loader.get_template('form.html')
        context = {}

        context['form'] = MyForm()

        return render(request, 'form.html', context)

    def post(self, request):
        context = {}
        form = MyForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            img = form.cleaned_data.get("image")
            img_path = img
            path = settings.MEDIA_ROOT+"/{}".format(img)
            form.save()

        context['name'] = name

        classes = load_csv_file()

        model = keras.models.load_model('D:\\Fils 4th year\\Licenta\\anaconda\\traffic_signs_classifier_model.h5')

        url = "http://127.0.0.1:8000/images/" + str(img_path)

        requests = req.get(url, stream=True)
        img = Image.open(requests.raw)

        context['image_uploaded'] = url

        image_width = 32 
        image_height = 32 
        image_channels_after_preprocessing = 1

        img = np.asarray(img)
        img = cv2.resize(img, (image_width, image_height))
        preprocessedImg = preprocessing(img)
        
        preprocessedImg = preprocessedImg.reshape(1, image_width, image_height, image_channels_after_preprocessing)

        threshold = 0.7

        probabilities = model.predict(preprocessedImg)
        for i in range(len(probabilities)):
            max_value = np.max(probabilities[i])

            if max_value < threshold:
                context['prediction_result'] = "Are you sure that the image contains a traffic sign?"
                print("Are you sure that the image contains a traffic sign?")
            else:
                prediction = model.predict_classes(preprocessedImg)
                print("Predicted sign: " + classes[int(prediction)])
                context['prediction_result'] = "Predicted sign: " + classes[int(prediction)]

        return render(request, 'form.html', context)