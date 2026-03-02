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