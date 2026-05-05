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

class ConnectionsWordInline(admin.TabularInline):
    model = ConnectionsWord
    extra = 4


class FramedGameDataInline(admin.TabularInline):
    model = FramedGameData
    extra = 6


@admin.register(Wordle)
class WordleAdmin(admin.ModelAdmin):
    list_display = ("date", "word")
    search_fields = ("word",)
    ordering = ("date",)


@admin.register(ConnectionsCategory)
class ConnectionsCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name", "connectionsword__word")
    inlines = [ConnectionsWordInline]


@admin.register(Connections)
class ConnectionsAdmin(admin.ModelAdmin):
    list_display = ("date",)
    filter_horizontal = ("categories",)
    ordering = ("date",)


@admin.register(Framed)
class FramedAdmin(admin.ModelAdmin):
    list_display = ("date", "paraula")
    search_fields = ("paraula",)
    ordering = ("date",)
    inlines = [FramedGameDataInline]


@admin.register(StatsWordle)
class StatsWordleAdmin(admin.ModelAdmin):
    list_display = ("user", "game", "completed", "attempts", "score", "time_taken")
    list_filter = ("completed",)
    search_fields = ("user__username", "game__word")


@admin.register(StatsConnections)
class StatsConnectionsAdmin(admin.ModelAdmin):
    list_display = ("user", "game", "completed", "points")
    list_filter = ("completed",)
    search_fields = ("user__username",)


@admin.register(StatsFramed)
class StatsFramedAdmin(admin.ModelAdmin):
    list_display = ("user", "game", "value", "completed", "guessed", "attempts", "points")
    list_filter = ("completed", "guessed")
    search_fields = ("user__username", "game__paraula", "value")
