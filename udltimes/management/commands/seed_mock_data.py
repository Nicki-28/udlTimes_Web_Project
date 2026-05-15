from datetime import timedelta

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

WORDLE_SEED_WORDS = [
    "REDES",
    "DATOS",
    "NODOS",
    "CACHE",
    "PIXEL",
    "CLICK",
    "TECLA",
    "PROXY",
    "LOGIN",
    "ADMIN",
    "INPUT",
    "PATCH",
    "STACK",
    "ERROR",
    "SHELL",
    "BATCH",
    "FIBER",
    "CIFRA",
    "GAMER",
    "SPAWN",
    "BUILD",
    "STATS",
    "QUEST",
    "LEVEL",
    "CRAFT",
    "GRIND",
    "SKINS",
    "MATCH",
    "CARRY",
    "NOOBS",
    "BUFFS",
    "NERFS",
    "AGGRO",
    "MELEE",
    "FRAME",
    "LOBBY",
    "GRAFO",
    "ROBOT",
    "MOVIL",
    "CHIPS",
    "MIRET",
    "MAGDA",
    "JOSEP",
    "NACHO",
    "SERGI",
    "PABLO",
    "ORIOL",
    "CORES",
    "ROUND",
    "BONUS",
    "SMOKE",
    "HILOS",
]


class Command(BaseCommand):
    help = "Create mock games for Wordle, Connections and Framed."

    def handle(self, *args, **options):
        today = timezone.localdate()

        self._seed_wordles(today)
        self._seed_connections(today)
        self._seed_frameds(today)
        self._seed_admin_user()
        self._seed_report_users()
        self._seed_mock_users_and_stats(today)

        self.stdout.write(self.style.SUCCESS("Mock data created or updated."))

    def _seed_admin_user(self):
        user, _ = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        user.is_staff = True
        user.is_superuser = True
        user.set_password("admin")
        user.save()

    def _seed_report_users(self):
        users = [
            ("sarrat", "sarrat123"),
            ("roberto", "roberto123"),
        ]

        for username, password in users:
            user, _ = User.objects.get_or_create(username=username)
            user.set_password(password)
            user.save()

    def _seed_wordles(self, today):
        for offset, word in enumerate(WORDLE_SEED_WORDS):
            Wordle.objects.update_or_create(
                date=today + timedelta(days=offset),
                defaults={"word": word.upper()},
            )

    def _seed_connections(self, today):
        games = [
            [
                ("Campus UdL", ["Rectorat", "Cappont", "ETSEA", "Salut"]),
                ("Vida universitaria", ["Apunts", "Examen", "Seminari", "Practica"]),
                ("Serveis", ["Biblioteca", "Campus", "Secretaria", "Sakai"]),
                ("Graus", ["Dret", "Medicina", "Informatica", "Lletres"]),
            ],
            [
                ("Espais", ["Aula", "Lab", "Bar", "Sala"]),
                ("Calendari", ["Parcial", "Final", "Entrega", "Tutoria"]),
                ("Material", ["Portatil", "Llibreta", "Boligraf", "Carpeta"]),
                ("Tramits", ["Matricula", "Beca", "Conveni", "Certificat"]),
            ],
            [
                ("Assignatures", ["Algebra", "Xarxes", "Fisica", "Programacio"]),
                ("Eines digitals", ["Git", "Docker", "Python", "Django"]),
                ("Avaluacio", ["Rubrica", "Projecte", "Practica", "Presentacio"]),
                ("Biblioteca", ["Prestec", "Silenci", "Taquilla", "Cataleg"]),
            ],
            [
                ("Campus Cappont", ["EPS", "Dret", "Aulari", "Polivalent"]),
                ("Tecnologia", ["Servidor", "Endpoint", "Branch", "Commit"]),
                ("Vida de classe", ["Apunts", "Lliurament", "Grup", "Tutoria"]),
                ("UdL colors", ["Grana", "Blanc", "Negre", "Daurat"]),
            ],
            [
                ("Rols projecte", ["Frontend", "Backend", "Disseny", "Testing"]),
                ("Dades", ["Seed", "Mock", "Json", "Fixture"]),
                ("Jocs", ["Wordle", "Framed", "Connections", "Leaderboard"]),
                ("Accions Git", ["Merge", "Push", "Pull", "Checkout"]),
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
            (
                "Rectorat",
                [
                    "https://i.ibb.co/1GLRm2sm/Rectorat-1-Aula.webp",
                    "https://i.ibb.co/Ld3rQY8Z/Rectorat-2-Parking.webp",
                    "https://i.ibb.co/27w3yQSX/Rectorat-3-Biblioteca.webp",
                    "https://i.ibb.co/DHpKyvvK/Rectorat-4-Edifici.webp",
                ],
            ),
            (
                "Biblioteca Jaume Porta",
                [
                    "https://i.ibb.co/gMZB3Gp9/Biblioteca-Jaume-Porta-1-Butaca.webp",
                    "https://i.ibb.co/q3hkBrMY/Biblioteca-Jaume-Porta-2-Taquilles.webp",
                    "https://i.ibb.co/20MZVYJ0/Biblioteca-Jaume-Porta-3-Auditori.webp",
                    "https://i.ibb.co/3mbPsk9p/Biblioteca-Jaume-Porta-4-Edifici.webp",
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
            ("jaume_mock", "Jaume Mock", 485, 390, 100),
            ("pol_mock", "Pol Mock", 430, 0, 80),
            ("nicole_mock", "Nicole Mock", 20, 30, 10),
            ("yasmin_mock", "Yasmin Mock", 10, 20, 0),
            ("nataly_mock", "Nataly Mock", 5, 10, 0),
            ("toni_mock", "Toni Mock", 0, 250, 0),
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
