from djangae.test import TestCase
from django.test import Client
from django.urls import reverse

from poll.models import Vote


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

    def test_create_vote(self):
        url = reverse("public:create-vote")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(Vote.objects.count(), 0)
        resp = self.client.post(
            url,
            data={
                "id_state": "AN",
                "id_country": "AU",
            },
        )
        # redirect on success
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Vote.objects.count(), 1)

    def test_vote_detail(self):
        url_create_vote = reverse("public:create-vote")
        resp = self.client.post(
            url_create_vote,
            data={
                "id_state": "AN",
                "id_country": "AU",
            },
        )
        # redirect on success which created vote entity
        self.assertEqual(resp.status_code, 302)

        vote = Vote.objects.first()
        url = reverse("public:cast-vote", kwargs={"vote_id": vote.pk})
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

        resp = self.client.post(
            url,
            data={
                "candidate": "NOT_CANDIDATE",
            },
        )
        # 403 - not a candidate
        self.assertEqual(resp.status_code, 403)

        resp = self.client.post(
            url,
            data={
                "candidate": Vote.ATIKU_ABUBAKAR,
            },
        )
        # redirect on success
        self.assertEqual(resp.status_code, 302)
        vote.refresh_from_db()
        self.assertEqual(vote.candidate, Vote.ATIKU_ABUBAKAR)

    def test_vote_success(self):
        url = reverse("public:vote-success")
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
