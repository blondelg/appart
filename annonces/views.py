from annonces.models import Annonce
from annonces.serializers import AnnonceSerializer
from rest_framework import viewsets
from rest_framework import permissions


class AnnonceViewSet(viewsets.ModelViewSet):
    queryset = Annonce.objects.all().order_by('-created_at')
    serializer_class = AnnonceSerializer
    permission_classes = [permissions.IsAuthenticated]