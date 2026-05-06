from django.contrib import admin

from .models import (
    Connections,
    ConnectionsCategory,
    ConnectionsWord,
    Framed,
    FramedConcept,
    FramedConceptImage,
    StatsConnections,
    StatsFramed,
    StatsWordle,
    Wordle,
)


class ConnectionsWordInline(admin.TabularInline):
    model = ConnectionsWord
    extra = 4


class FramedConceptImageInline(admin.TabularInline):
    model = FramedConceptImage
    extra = 4


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


@admin.register(FramedConcept)
class FramedConceptAdmin(admin.ModelAdmin):
    list_display = ("concept", "description")
    search_fields = ("concept",)
    inlines = [FramedConceptImageInline]


@admin.register(Framed)
class FramedAdmin(admin.ModelAdmin):
    list_display = ("date", "concept")
    search_fields = ("concept__concept",)
    ordering = ("date",)


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
    list_display = ("user", "game", "guessed", "images_needed", "points")
    list_filter = ("guessed",)
    search_fields = ("user__username", "game__concept__concept")


@admin.register(ConnectionsWord)
class ConnectionsWordAdmin(admin.ModelAdmin):
    list_display = ("category", "word")
    search_fields = ("category__name", "word")


@admin.register(FramedConceptImage)
class FramedConceptImageAdmin(admin.ModelAdmin):
    list_display = ("concept", "order", "image_url")
    list_filter = ("concept",)
    ordering = ("concept", "order")
