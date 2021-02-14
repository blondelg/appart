import unittest
from datetime import datetime, date

import django
from django.contrib.auth.models import User
from django.test import Client
from annonces.models import Annonce


class AnnonceTest(unittest.TestCase):
    def setUp(self):
        try:
            self.user = User.objects.create_superuser('admin', 'admin')
        except:
            pass
        self.client = Client()
        self.client.login(username='admin', password='admin')
        self.data_url = "https://someadd.com"
        self.data_add = {
            'titre': 'Annonce de test',
            'prix': 400000,
            'surface': 40,
            'description': 'Description de test',
            'code_postal': '75017',
            'date_publication': date(2012, 10, 23),
            'status': 'VALIDE'
        }

    def test_save_url(self):
        # Given
        try:
            add = Annonce.objects.get(lien=self.data_url)
            add.delete()
        except:
            pass
        add = Annonce()
        add.lien = self.data_url
        add.save()

        # When
        add = Annonce.objects.get(lien=self.data_url)

        # Then
        self.assertEqual(add.lien, self.data_url)


    def test_save_url_twice(self):
        # Given
        try:
            add = Annonce.objects.get(lien=self.data_url)
            add.delete()
        except:
            pass
        add = Annonce()
        add.lien = self.data_url
        add.save()

        # When
        add_2 = Annonce(lien=self.data_url)

        # Then
        with self.assertRaises(django.db.utils.IntegrityError):
            add_2.save()


    def test_save_annonce(self):
        # Given/ When
        Annonce.objects.filter(lien=self.data_url).update(**self.data_add)

        # Then
        self.assertEqual(Annonce.objects.get(lien=self.data_url).titre, self.data_add['titre'])


    def test_get_add_view(self):
        # Given
        try:
            add = Annonce.objects.get(lien=self.data_url)
            add.delete()
        except:
            pass
        add = Annonce()
        add.lien = self.data_url
        add.save()

        #When
        response = self.client.get("/annonces/")

        #Then
        self.assertEqual(response.status_code, 200)