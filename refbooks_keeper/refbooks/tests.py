from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls import reverse
from .models import Version, Refbook
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
        self.test_element = [{
            "code": "L96",
            "value": "1 element of 1 ref and 2 ver"
        }]

    def get_response(self, basename, args: list, params: dict):
        response = self.client.get(
            reverse(basename, args=args),
            params,
            HTTP_ACCEPT='application/json'
        )
        return response

    def test_refbooks(self):
        response = self.get_response('refbook-list', [], {})
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
        response = self.get_response('refbook-list', [], {'date': target_date})

        self.assertEqual(response.status_code, 204)

    def test_refbooks_by_date(self):
        target_date = self.curr_date - timedelta(days=3)
        response = self.get_response('refbook-list', [], {'date': target_date})
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
        response = self.get_response('refbook-elements', ['1'], {})
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
        response = self.get_response('refbook-elements', ['1'],
                                     {'version': '2.0'})
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
        response = self.get_response('refbook-elements', ['1'],
                                     {'version': '3.0'})

        self.assertEqual(response.status_code, 404)

    def test_elements_no_refbook(self):
        response = self.get_response('refbook-elements', ['3'],
                                     {'version': '3.0'})

        self.assertEqual(response.status_code, 404)

    def test_ckeck_element(self):
        response = self.get_response(
            'refbook-check-element',
            [1],
            {
                'code': "L96",
                'value': "1 element of 1 ref and 2 ver",
                'version': "1.0"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, self.test_element)

    def test_ckeck_element_no_version(self):
        response = self.get_response(
            'refbook-check-element',
            [1],
            {
                'code': "L96",
                'value': "1 element of 1 ref and 2 ver"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, self.test_element)

    def test_ckeck_element_no_code(self):
        response = self.get_response(
            'refbook-check-element',
            [1],
            {
                'value': "1 element of 1 ref and 2 ver"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, self.test_element)

    def test_ckeck_element_no_value(self):
        response = self.get_response(
            'refbook-check-element',
            [1],
            {
                'code': "L96"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, self.test_element)

    def test_ckeck_element_wrong_code(self):
        response = self.get_response(
            'refbook-check-element',
            [1],
            {
                'code': "T96",
            }
        )

        self.assertEqual(response.status_code, 404)

    def test_ckeck_element_wrong_value(self):
        response = self.get_response(
            'refbook-check-element',
            [1],
            {
                'value': "wrong value"
            }
        )

        self.assertEqual(response.status_code, 404)

    def test_ckeck_element_wrong_exist_version(self):
        response = self.get_response(
            'refbook-check-element',
            [1],
            {
                'code': "L96",
                'value': "1 element of 1 ref and 2 ver",
                'version': "2.0"
            }
        )

        self.assertEqual(response.status_code, 404)

    def test_ckeck_element_wrong_not_exist_version(self):
        response = self.get_response(
            'refbook-check-element',
            [1],
            {
                'code': "L96",
                'value': "1 element of 1 ref and 2 ver",
                'version': "3.0"
            }
        )
        self.assertEqual(response.status_code, 404)

    def test_ckeck_element_wrong_exist_refbook(self):
        response = self.get_response(
            'refbook-check-element',
            [2],
            {
                'code': "L96",
                'value': "1 element of 1 ref and 2 ver",
                'version': "1.0"
            }
        )

        self.assertEqual(response.status_code, 404)

    def test_ckeck_element_wrong_not_exist_refbook(self):
        response = self.get_response(
            'refbook-check-element',
            [3],
            {
                'code': "L96",
                'value': "1 element of 1 ref and 2 ver",
                'version': "1.0"
            }
        )

        self.assertEqual(response.status_code, 404)

    def test_refbook_code_constraint(self):
        with self.assertRaises(IntegrityError):
            db_refbook = Refbook.objects.get(id=1)
            refbook = Refbook.objects.create(
                code=db_refbook.code,
                owner=db_refbook.owner
            )
            refbook.save()

    def test_version_name_and_refbook_constraint(self):
        with self.assertRaises(IntegrityError):
            db_version = Version.objects.get(id=1)
            version = Version.objects.create(
                refbook=db_version.refbook,
                name=db_version.name
            )
            version.save()

    def test_version_date_and_refbook_constraint(self):
        with self.assertRaises(IntegrityError):
            db_version = Version.objects.get(id=1)
            version = Version.objects.create(
                refbook=db_version.refbook,
                start_date=db_version.start_date
            )
            version.save()
