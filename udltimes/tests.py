import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from udltimes.models import (
    Connections,
    ConnectionsCategory,
    ConnectionsWord,
    Framed,
    FramedGameData,
    StatsFramed,
    StatsWordle,
    Wordle,
)


class GameApiTests(TestCase):
    def setUp(self):
        self.today = timezone.localdate()
        self.user = User.objects.create_user(username="jaume", password="testpass123")

    def test_wordle_guess_scores_and_blocks_completed_user(self):
        game = Wordle.objects.create(date=self.today, word="AULAS")
        self.client.login(username="jaume", password="testpass123")

        response = self.client.post(
            reverse("api_wordle_guess"),
            data=json.dumps({"guess": "AULAS"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["colors"], ["green"] * 6)
        self.assertTrue(StatsWordle.objects.filter(user=self.user, game=game).exists())

        repeated = self.client.post(
            reverse("api_wordle_guess"),
            data=json.dumps({"guess": "AULAS"}),
            content_type="application/json",
        )
        self.assertEqual(repeated.status_code, 409)

    def test_connections_guess_detects_category(self):
        game = Connections.objects.create(date=self.today)
        category = ConnectionsCategory.objects.create(name="Campus UdL")
        for word in ["Rectorat", "Cappont", "ETSEA", "Salut"]:
            ConnectionsWord.objects.create(category=category, word=word)
        game.categories.add(category)

        response = self.client.post(
            reverse("api_connections_guess"),
            data=json.dumps({"words": ["Salut", "ETSEA", "Cappont", "Rectorat"]}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["correct"])
        self.assertEqual(response.json()["category"], "Campus UdL")

    def test_framed_correct_guess_saves_completion_for_logged_user(self):
        game = Framed.objects.create(date=self.today, paraula="Rectorat")
        FramedGameData.objects.create(game=game, order=1, image="https://example.com/rectorat.jpg")
        self.client.login(username="jaume", password="testpass123")

        response = self.client.post(
            reverse("api_framed_guess"),
            data=json.dumps({"guess": "rectorat"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["correct"])
        self.assertTrue(StatsFramed.objects.filter(user=self.user, game=game).exists())
