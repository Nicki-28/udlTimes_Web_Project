from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
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


class Command(BaseCommand):
    help = "Create mock games for Wordle, Connections and Framed."

    def handle(self, *args, **options):
        today = timezone.localdate()

        self._seed_wordles(today)
        self._seed_connections(today)
        self._seed_frameds(today)
        self._seed_mock_users_and_stats(today)

        self.stdout.write(self.style.SUCCESS("Mock data created or updated."))

    def _seed_wordles(self, today):
        words = self._load_wordle_words()
        for offset, word in enumerate(words):
            Wordle.objects.update_or_create(
                date=today + timedelta(days=offset),
                defaults={"word": word.upper()},
            )

    def _load_wordle_words(self):
        words_path = settings.BASE_DIR / "templates" / "wordle" / "words.txt"
        fallback_words = ["AULAS", "BECAS", "LIBRO", "TESIS", "NOTAS"]

        try:
            words = [
                line.strip().upper()
                for line in words_path.read_text(encoding="utf-8").splitlines()
                if len(line.strip()) == 5
            ]
        except FileNotFoundError:
            words = fallback_words

        return words or fallback_words

    def _seed_connections(self, today):
        games = [
            [
                ("Campus UdL", ["Rectorat", "Cappont", "ETSEA", "Salut"]),
                ("Vida universitaria", ["Apunts", "Examen", "Seminari", "Practica"]),
                ("Serveis", ["Biblioteca", "Campus", "Secretaria", "Moodle"]),
                ("Graus", ["Dret", "Medicina", "Informatica", "Lletres"]),
            ],
            [
                ("Espais", ["Aula", "Lab", "Bar", "Sala"]),
                ("Calendari", ["Parcial", "Final", "Entrega", "Tutoria"]),
                ("Material", ["Portatil", "Llibreta", "Boligraf", "Carpeta"]),
                ("Tramits", ["Matricula", "Beca", "Conveni", "Certificat"]),
            ],
        ]

        for offset, game_categories in enumerate(games):
            game, _ = Connections.objects.get_or_create(date=today + timedelta(days=offset))
            category_objects = []

            for category_name, words in game_categories:
                category, _ = ConnectionsCategory.objects.get_or_create(name=category_name)
                for word in words:
                    ConnectionsWord.objects.get_or_create(category=category, word=word)
                category_objects.append(category)

            game.categories.set(category_objects)

    def _seed_frameds(self, today):
        games = [
            (
                "EPS",
                [
                    "https://i.ibb.co/CpzBLHHh/EPS-1-Aula.webp",
                    "https://i.ibb.co/Ndm6WybY/EPS-2-Macs.webp",
                    "https://i.ibb.co/hF5h3kjX/EPS-3-Mural.webp",
                    "https://i.ibb.co/SDCbKtWd/EPS-4-EPS.webp",
                ],
            ),
            (
                "Facultat Dret",
                [
                    "https://i.ibb.co/1JQtCHrD/Facultat-Dret-1-Aula.webp",
                    "https://i.ibb.co/rKF4JfsT/Facultat-Dret-2-Curvatura.webp",
                    "https://i.ibb.co/kgqwfJmc/Facultat-Dret-3-Plano.webp",
                    "https://i.ibb.co/FL78gC9M/Facultat-Dret-4-Entrada.webp",
                ],
            ),
            (
                "Polivalent",
                [
                    "https://i.ibb.co/kgD4H63J/Polivalent-1-Aula.webp",
                    "https://i.ibb.co/1GJspRwX/Polivalent-2-Examen.webp",
                    "https://i.ibb.co/TBM7QB03/Polivalent-3-Entrada.webp",
                    "https://i.ibb.co/QvdtfWh8/Polivalent-4-Polivalent.webp",
                ],
            ),
        ]

        for offset, (answer, images) in enumerate(games):
            concept, _ = FramedConcept.objects.update_or_create(
                concept=answer,
                defaults={"description": f"Mock Framed answer for {answer}."},
            )
            framed, _ = Framed.objects.update_or_create(
                date=today + timedelta(days=offset),
                defaults={"concept": concept},
            )

            for order, image_url in enumerate(images, start=1):
                FramedConceptImage.objects.update_or_create(
                    concept=concept,
                    order=order,
                    defaults={"image_url": image_url},
                )

            FramedConceptImage.objects.filter(concept=concept, order__gt=len(images)).delete()

    def _seed_mock_users_and_stats(self, today):
        users_data = [
            ("anna_mock", "Anna Mock", 485, 390, 100),
            ("pol_mock", "Pol Mock", 430, 250, 80),
            ("nicole_mock", "Nicole Mock", 370, 400, 70),
            ("yasmin_mock", "Yasmin Mock", 315, 300, 40),
            ("nataly_mock", "Nataly Mock", 260, 150, 30),
            ("toni_mock", "Toni Mock", 210, 100, 0),
        ]

        wordles = list(Wordle.objects.filter(date__gte=today).order_by("date")[:5])
        connections = list(Connections.objects.filter(date__gte=today).order_by("date")[:2])
        frameds = list(Framed.objects.filter(date__gte=today).order_by("date")[:3])

        for index, (username, full_name, wordle_total, connections_total, framed_total) in enumerate(users_data):
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": f"{username}@example.com",
                    "first_name": full_name,
                },
            )
            if created:
                user.set_password("mockpass123")
                user.save()

            self._seed_wordle_stats(user, wordles, wordle_total, index)
            self._seed_connections_stats(user, connections, connections_total, index)
            self._seed_framed_stats(user, frameds, framed_total, index)

    def _seed_wordle_stats(self, user, games, total_score, user_index):
        if not games:
            return

        base_score = total_score // len(games)
        remainder = total_score % len(games)

        for game_index, game in enumerate(games):
            score = base_score + (1 if game_index < remainder else 0)
            StatsWordle.objects.update_or_create(
                user=user,
                game=game,
                defaults={
                    "completed": True,
                    "attempts": min(6, 1 + ((user_index + game_index) % 5)),
                    "score": score,
                    "time_taken": 45 + (user_index * 18) + (game_index * 11),
                },
            )

    def _seed_connections_stats(self, user, games, total_points, user_index):
        if not games:
            return

        base_points = total_points // len(games)
        remainder = total_points % len(games)

        for game_index, game in enumerate(games):
            points = base_points + (1 if game_index < remainder else 0)
            StatsConnections.objects.update_or_create(
                user=user,
                game=game,
                defaults={
                    "completed": points > 0,
                    "points": points,
                },
            )

    def _seed_framed_stats(self, user, games, total_points, user_index):
        if not games:
            return

        base_points = total_points // len(games)
        remainder = total_points % len(games)

        for game_index, game in enumerate(games):
            points = base_points + (1 if game_index < remainder else 0)
            StatsFramed.objects.update_or_create(
                user=user,
                game=game,
                defaults={
                    "images_needed": min(4, 1 + ((user_index + game_index) % 4)),
                    "guessed": points > 0,
                    "points": points,
                },
            )
