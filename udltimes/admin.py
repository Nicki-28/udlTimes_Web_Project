from django.contrib import admin

# Register your models here.

from .models import (
    Wordle,
    StatsWordle,
    Framed,
    StatsFramed,
    FramedConcept,
    FramedConceptImage,
    ConnectionsWord,
    StatsConnections,
    ConnectionsCategory,
    Connections,
)

admin.site.register(Wordle)
admin.site.register(StatsWordle)
admin.site.register(Framed)
admin.site.register(FramedConcept)
admin.site.register(FramedConceptImage)
admin.site.register(StatsFramed)
admin.site.register(ConnectionsCategory)
admin.site.register(ConnectionsWord)
admin.site.register(StatsConnections)
admin.site.register(Connections)
