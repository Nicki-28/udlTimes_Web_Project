from django.db import migrations, models


def mark_existing_framed_stats_completed(apps, schema_editor):
    StatsFramed = apps.get_model('udltimes', 'StatsFramed')
    StatsFramed.objects.filter(value__gt='').update(
        completed=True,
        guessed=True,
        attempts=1,
        points=60,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('udltimes', '0003_statswordle_attempts_score_time_taken'),
    ]

    operations = [
        migrations.AddField(
            model_name='statsframed',
            name='attempts',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='statsframed',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='statsframed',
            name='guessed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='statsframed',
            name='points',
            field=models.IntegerField(default=0),
        ),
        migrations.RunPython(mark_existing_framed_stats_completed, migrations.RunPython.noop),
    ]
