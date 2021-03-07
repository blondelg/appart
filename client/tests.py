import unittest

from client.core import TorClient
from rest_framework.status import HTTP_200_OK


class AnnonceTest(unittest.TestCase):
    def setUp(self):
        self.tor_client = TorClient()

    def test_tor_client(self):
        # Given/ When
        response = self.tor_client.get("https://www.google.fr")

        # Then
        self.assertEqual(response.status_code, HTTP_200_OK)
