from django.core.management.base import BaseCommand
from annonces.models import Annonce


class Command(BaseCommand):
    for add in Annonce.objects.filter(status='ERREUR'):
        print(f"Deleted : {add.lien}")
        add.delete()