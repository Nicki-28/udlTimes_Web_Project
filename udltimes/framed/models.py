from django.db import models
from django.contrib.auth.models import User

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
