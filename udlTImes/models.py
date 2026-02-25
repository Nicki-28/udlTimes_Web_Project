from django.db import models
from django.contrib.auth.models import User
# User

class User(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# Wordle

class Wordle(models.Model):
    word = models.CharField(max_length=100)
    date = models.DateField(unique=True)


class StatsWordle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Wordle, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)


# Framed

class Framed(models.Model):
    id_paraula = models.CharField(max_length=100, unique=True)
    paraula = models.CharField(max_length=100)
    date = models.DateField(unique=True)


class StatsFramed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_game = models.ForeignKey(Framed, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)


class FramedGameData(models.Model):
    id_game = models.ForeignKey(Framed, on_delete=models.CASCADE)
    order = models.IntegerField()
    image = models.CharField(max_length=1000)


# Connections

class Connections(models.Model):
    date = models.DateField(unique=True)


class ConnectionsWord(models.Model):
    id_category = models.ForeignKey(Connections, on_delete=models.CASCADE)
    word = models.CharField(max_length=100)


class StatsConnections(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Connections, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
