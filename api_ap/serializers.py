from rest_framework import serializers

from api_ap.models import Franchise, Quiosque

from scraper.scrap_functions import scrap_from_db


class FranchiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Franchise
        fields = '__all__'

    def list(self, request):
        scrap_from_db()
        return Franchise.objects.all()


class QuiosqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiosque
        fields = '__all__'