from django.contrib import admin

# Register your models here.

from .models import (
    Wordle,
    StatsWordle,
    Framed,
    StatsFramed,
    FramedGameData,
    ConnectionsWord,
    StatsConnections,
    ConnectionsCategory,
    Connections,
)

admin.site.register(Wordle)
admin.site.register(StatsWordle)
admin.site.register(Framed)
admin.site.register(FramedGameData)
admin.site.register(StatsFramed)
admin.site.register(ConnectionsCategory)
admin.site.register(ConnectionsWord)
admin.site.register(StatsConnections)
admin.site.register(Connections)
