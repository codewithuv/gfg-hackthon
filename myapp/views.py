from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.http import HttpResponse
import pickle
import numpy as np
import pandas as pd
import os

# Use raw string for Windows paths
scaler_path = r"U:\gfg hackthon\health\Model\standardScalar.pkl"
model_path = r"U:\gfg hackthon\health\Model\modelForPrediction.pkl"

# Load models and scaler
scaler = pickle.load(open(scaler_path, "rb"))
model = pickle.load(open(model_path, "rb"))

def index(request):
    return render(request, 'index.html')
def home(request):
    return render(request,'home.html')
def index1(request):
    return render(request,'index1.html')
@csrf_protect
def predict_datapoint(request):
    result = ""
    if request.method == 'POST':
        Pregnancies = int(request.POST.get("Pregnancies"))
        Glucose = float(request.POST.get('Glucose'))
        BloodPressure = float(request.POST.get('BloodPressure'))
        SkinThickness = float(request.POST.get('SkinThickness'))
        Insulin = float(request.POST.get('Insulin'))
        BMI = float(request.POST.get('BMI'))
        DiabetesPedigreeFunction = float(request.POST.get('DiabetesPedigreeFunction'))
        Age = float(request.POST.get('Age'))

        new_data = scaler.transform([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])
        predict = model.predict(new_data)
    
        result = 'Diabetic' if predict[0] == 1 else 'Non-Diabetic'
         
        return render(request, 'single_prediction.html', {'result': result})
    else:
        return render(request, 'home.html')
