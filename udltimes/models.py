from django.db import models
from django.contrib.auth.models import User

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


# Framed

class FramedConcept(models.Model):
    concept = models.CharField(max_length=200, unique=True)
    description = models.CharField(blank=True)

    def __str__(self):
        return self.concept
    
class FramedConceptImage(models.Model):
    concept = models.ForeignKey(FramedConcept, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField(max_length=500)
    order =  models.PositiveBigIntegerField()

    class Meta:
        ordering = ['order'] # 1->4 : dificil -> facil
        unique_together = ('concept', 'order')

    def __str__(self):
        return f"{self.concept.concept} - imagen {self.order}"


class Framed(models.Model): #Juego del dia
    date = models.DateField(primary_key=True)
    concept = models.ForeignKey(FramedConcept, on_delete= models.CASCADE, related_name='games', blank=True)

    def __str__(self):
        return f"{self.date} - {self.concept.concept}"



class StatsFramed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Framed, on_delete=models.CASCADE)
    images_needed = models.PositiveSmallIntegerField(null=True, blank=True)
    guessed = models.BooleanField(default=False)
    #value = models.CharField(max_length=100)

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return f"{self.user} - {self.game}"


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





