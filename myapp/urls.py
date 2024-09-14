from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('predict_datapoint/', views.predict_datapoint, name='predict_datapoint'),
    path('home',views.home),
    path('a',views.index1)
]
