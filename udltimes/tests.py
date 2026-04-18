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
    FramedConcept,
    FramedConceptImage,
    StatsConnections,
    StatsFramed,
    StatsWordle,
    Wordle,
)


class GameApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='jaume', password='secret123')
        self.client.force_login(self.user)
        today = timezone.localdate()

        self.wordle = Wordle.objects.create(date=today, word='campus')

        self.connections = Connections.objects.create(date=today)
        self.category_names = ['Professors', 'Buildings', 'Degrees', 'Libraries']
        self.connection_words = {
            'Professors': ['Pol', 'Toni', 'Yasmin', 'Nicole'],
            'Buildings': ['Rectorat', 'Biblioteca', 'Aulari', 'Campus'],
            'Degrees': ['Informatics', 'Math', 'Law', 'Medicine'],
            'Libraries': ['Study', 'Books', 'Quiet', 'Loans'],
        }
        for category_name in self.category_names:
            category = ConnectionsCategory.objects.create(name=category_name)
            for word in self.connection_words[category_name]:
                ConnectionsWord.objects.create(category=category, word=word)
            self.connections.categories.add(category)

        self.framed_concept = FramedConcept.objects.create(
            concept='Rectorat',
            description='Main administration building',
        )
        for order in range(1, 5):
            FramedConceptImage.objects.create(
                concept=self.framed_concept,
                image_url=f'https://example.com/image-{order}.jpg',
                order=order,
            )
        self.framed = Framed.objects.create(date=today, concept=self.framed_concept)

    def test_wordle_today_endpoint_returns_length(self):
        response = self.client.get(reverse('api_wordle_today'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['length'], len(self.wordle.word))
        self.assertFalse(response.json()['already_completed'])

    def test_wordle_check_saves_stat_when_correct(self):
        response = self.client.post(
            reverse('api_wordle_check'),
            data=json.dumps({'guess': 'campus'}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['correct'])
        self.assertTrue(
            StatsWordle.objects.filter(user=self.user, game=self.wordle, completed=True).exists()
        )

    def test_wordle_check_blocks_repeat_after_completion(self):
        StatsWordle.objects.create(user=self.user, game=self.wordle, completed=True)

        response = self.client.post(
            reverse('api_wordle_check'),
            data=json.dumps({'guess': 'campus'}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 409)
        self.assertTrue(response.json()['already_completed'])

    def test_connections_today_endpoint_returns_all_words(self):
        response = self.client.get(reverse('api_connections_today'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['words']), 16)
        self.assertFalse(response.json()['already_completed'])

    def test_connections_check_accepts_valid_group(self):
        response = self.client.post(
            reverse('api_connections_check'),
            data=json.dumps({'words': self.connection_words['Professors']}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['correct'])
        self.assertEqual(response.json()['category'], 'Professors')

    def test_connections_complete_saves_stat(self):
        response = self.client.post(
            reverse('api_connections_complete'),
            data=json.dumps({'solved_count': 4}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['saved'])
        self.assertTrue(
            StatsConnections.objects.filter(
                user=self.user,
                game=self.connections,
                completed=True,
            ).exists()
        )

    def test_connections_complete_blocks_repeat_after_completion(self):
        StatsConnections.objects.create(user=self.user, game=self.connections, completed=True)

        response = self.client.post(
            reverse('api_connections_complete'),
            data=json.dumps({'solved_count': 4}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 409)
        self.assertTrue(response.json()['already_completed'])

    def test_framed_today_endpoint_returns_images_and_options(self):
        response = self.client.get(reverse('api_framed_today'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['images']), 4)
        self.assertIn('Rectorat', response.json()['options'])
        self.assertFalse(response.json()['already_completed'])

    def test_framed_check_saves_stat_when_correct(self):
        response = self.client.post(
            reverse('api_framed_check'),
            data=json.dumps({'guess': 'Rectorat', 'images_needed': 2}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['correct'])
        self.assertTrue(
            StatsFramed.objects.filter(
                user=self.user,
                game=self.framed,
                guessed=True,
                images_needed=2,
            ).exists()
        )

    def test_framed_check_blocks_repeat_after_completion(self):
        StatsFramed.objects.create(user=self.user, game=self.framed, guessed=True, images_needed=2)

        response = self.client.post(
            reverse('api_framed_check'),
            data=json.dumps({'guess': 'Rectorat', 'images_needed': 2}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 409)
        self.assertTrue(response.json()['already_completed'])
