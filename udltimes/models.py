from django.db import models
from django.contrib.auth.models import User

# Wordle

class Wordle(models.Model):
    date = models.DateField(primary_key=True)
    word = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.date} - {self.word}"


class StatsWordle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Wordle, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return f"{self.user} - {self.game}"


# Framed

class Framed(models.Model):
    date = models.DateField(primary_key=True)
    paraula = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.date} - {self.paraula}"

class FramedGameData(models.Model):
    game = models.ForeignKey(Framed, on_delete=models.CASCADE)
    order = models.IntegerField()
    image = models.CharField(max_length=1000)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["game", "order"], name="unique_game_order_framedgamedata")]

    def __str__(self):
        return f"{self.game} - Image {self.order}"

class StatsFramed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Framed, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "game"], name="unique_user_game_statsframed")]

    def __str__(self):
        return f"{self.user} - {self.game}"



# Connections

class ConnectionsCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ConnectionsWord(models.Model):
    category = models.ForeignKey(ConnectionsCategory, on_delete=models.CASCADE)
    word = models.CharField(max_length=100)

    class Meta:
        unique_together = ("category", "word")

    def __str__(self):
        return f"{self.category} - {self.word}"


class Connections(models.Model):
    date = models.DateField(primary_key=True)
    categories = models.ManyToManyField(ConnectionsCategory, related_name="games")

    def __str__(self):
        cats = ", ".join([c.name for c in self.categories.all()])
        return f"Connections {self.date} ({cats})"


class StatsConnections(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Connections, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "game")

    def __str__(self):
        return f"{self.user} - {self.game}"
