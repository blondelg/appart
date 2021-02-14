from django.core.management.base import BaseCommand
from pap.toolbox import GetUrls, LoadData
from annonces.models import Annonce


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            help='Target url to request to get add lists',
        )

        parser.add_argument(
            '--get-urls',
            action='store_true',
            help='Load add urls from a search view.',
        )

        parser.add_argument(
            '--load-adds',
            action='store_true',
            help='Load add datas from urls.',
        )

    def handle(self, *args, **options):
        if options['get_urls']:
            try:
                url = options['url']
            except:
                raise (KeyError("Il manque l'url."))

            GetUrls(url)

        if options['load_adds']:
            for add in Annonce.objects.filter(status='ATTENTE'):
                LoadData(add.lien)


