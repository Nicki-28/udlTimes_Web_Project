from django.contrib import admin

# Register your models here.

from .models import (
    User,
    Wordle,
    StatsWordle,
    Framed,
    StatsFramed,
    FramedGameData,
    Connections,
    ConnectionsWord,
    StatsConnections,
)

admin.site.register(User)
admin.site.register(Wordle)
admin.site.register(StatsWordle)
admin.site.register(Framed)
admin.site.register(StatsFramed)
admin.site.register(FramedGameData)
admin.site.register(Connections)
admin.site.register(ConnectionsWord)
admin.site.register(StatsConnections)
