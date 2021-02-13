from rest_framework import serializers
from annonces.models import Annonce


class AnnonceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annonce
        fields = '__all__'