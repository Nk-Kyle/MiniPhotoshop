from django.urls import path
from .views import *

urlpatterns = [
    path('rotateRight/', rotateRight),
    path('rotateLeft/',rotateLeft),
    path('horizontalFlip/',horizontalFlip),
    path('verticalFlip/', verticalFlip),
    path('zoomOut/', zoomOut),
    path('zoomIn/', zoomIn),
    path('grayScale/', grayScale),
    path('negative/', negative),
    path('complement/', complement),
    path('brighten/', brighten),
    path('contrast/', contrast),
    path('log/', log),
    path('exp/', exp)
]