from djangae.test import TestCase
from django.test import Client
from django.urls import reverse


class PublicTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        super().setUp()

    def test_index_page(self):
        url = reverse("public:index")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_about_page(self):
        url = reverse("public:about")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
