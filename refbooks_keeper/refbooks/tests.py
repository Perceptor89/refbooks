from django.test import TestCase
from django.urls import reverse
from .models import Version
from datetime import datetime, timedelta


class TestRefbooks(TestCase):
    fixtures = [
        'users.json',
        'refbooks.json',
        'versions.json',
        'elements.json'
    ]

    def setUp(self):
        self.curr_date = datetime.now().date()
        version_1 = Version.objects.get(id=1)
        version_1.start_date = self.curr_date - timedelta(days=10)
        version_1.save()
        version_2 = Version.objects.get(id=2)
        version_2.start_date = self.curr_date - timedelta(days=2)
        version_2.save()
        version_3 = Version.objects.get(id=3)
        version_3.start_date = str(self.curr_date + timedelta(days=2))
        version_3.save()

    def test_refbook(self):
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

    def test_refbooks_by_date_no_content(self):
        target_date = self.curr_date - timedelta(days=11)
        response = self.client.get(
            reverse('refbook-list'),
            {'date': target_date},
            HTTP_ACCEPT='application/json'
        )
        print(response.data)
        self.assertEqual(response.status_code, 204)

    def test_refbooks_by_date(self):
        target_date = self.curr_date - timedelta(days=3)
        response = self.client.get(
            reverse('refbook-list'),
            {'date': target_date},
            HTTP_ACCEPT='application/json'
        )
        target_result = {
            "refbooks": [
                {
                    "id": "2",
                    "code": "ICD-10",
                    "name": " -10"
                }
            ]
        }
        self.assertEqual(response.data, target_result)

    def test_elements_no_version(self):
        response = self.client.get(
            reverse('refbook-elements', args=['1']),
            HTTP_ACCEPT='application/json'
        )
        target_result = {
            "elements": [
                {
                    "code": "L96",
                    "value": "1 element of 1 ref and 2 ver"
                },
                {
                    "code": "D23",
                    "value": "2 element of 1 ref and 2 ver"
                }
            ]
        }
        self.assertEqual(response.data, target_result)

    def test_elements_by_version(self):
        response = self.client.get(
            reverse('refbook-elements', args=['1']),
            {'version': '2.0'},
            HTTP_ACCEPT='application/json'
        )
        target_result = {
            "elements": [
                {
                    "code": "G14",
                    "value": "1 element of 1 ref and 3 ver"
                },
                {
                    "code": "T12",
                    "value": "2 element of 1 ref and 3 ver"
                }
            ]
        }
        self.assertEqual(response.data, target_result)

    def test_elements_by_version_no_content(self):
        response = self.client.get(
            reverse('refbook-elements', args=['1']),
            {'version': '3.0'},
            HTTP_ACCEPT='application/json'
        )
        self.assertEqual(response.status_code, 204)
