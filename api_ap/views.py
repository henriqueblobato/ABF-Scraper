from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from api_ap.models import Franchise, Quiosque
from api_ap.serializers import FranchiseSerializer, QuiosqueSerializer


class FranchiseViewSet(viewsets.ModelViewSet):
    queryset = Franchise.objects.all()
    serializer_class = FranchiseSerializer


class QuiosqueViewSet(viewsets.ModelViewSet):
    queryset = Quiosque.objects.all()
    serializer_class = QuiosqueSerializer