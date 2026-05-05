from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from udltimes.models import (
    Connections,
    ConnectionsCategory,
    ConnectionsWord,
    Framed,
    FramedGameData,
    Wordle,
)


class Command(BaseCommand):
    help = "Create mock games for Wordle, Connections and Framed."

    def handle(self, *args, **options):
        today = timezone.localdate()

        self._seed_wordles(today)
        self._seed_connections(today)
        self._seed_frameds(today)

        self.stdout.write(self.style.SUCCESS("Mock data created or updated."))

    def _seed_wordles(self, today):
        words = ["AULAS", "BECAS", "LIBRO", "TESIS", "NOTAS"]
        for offset, word in enumerate(words):
            Wordle.objects.update_or_create(
                date=today + timedelta(days=offset),
                defaults={"word": word},
            )

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
            framed, _ = Framed.objects.update_or_create(
                date=today + timedelta(days=offset),
                defaults={"paraula": answer},
            )

            for order, image in enumerate(images, start=1):
                FramedGameData.objects.update_or_create(
                    game=framed,
                    order=order,
                    defaults={"image": image},
                )
