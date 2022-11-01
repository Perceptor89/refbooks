from django.test import TestCase
from django.urls import reverse
from .models import Refbook
import urllib.parse as urlparse


class TestRefbooks(TestCase):
    fixtures = [
        'users.json',
        'refbooks.json',
        'versions.json'
    ]

    def setUp(self):
        self.refbook_1 = Refbook.objects.get(id=1)
        self.refbook_2 = Refbook.objects.get(id=2)

    def test_refbook_list(self):
        response = self.client.get(reverse('refbook-list'))
        target_result = {
            "refbooks": [
                {
                    "id": "1",
                    "code": "MS1",
                    "name": " "
                },
                {
                    "id": "2",
                    "code": "ICD-10",
                    "name": " -10"
                },
            ]
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, target_result)

    def test_refbook_list_with_date(self):
        url = reverse('refbook-list')

        params = urlparse.urlencode({'date': '2022-10-27'})
        target_url = f'{url}?{params}'
        response = self.client.get(target_url)
        target_result = {'refbooks': []}
        self.assertEqual(response.data, target_result)

        params = urlparse.urlencode({'date': '2022-10-28'})
        target_url = f'{url}?{params}'
        response = self.client.get(target_url)
        target_result = {
            "refbooks": [
                {
                    "id": "1",
                    "code": "MS1",
                    "name": " "
                }
            ]
        }
        self.assertEqual(response.data, target_result)
