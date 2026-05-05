from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('udltimes', '0002_statsconnections_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='statswordle',
            name='attempts',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='statswordle',
            name='score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='statswordle',
            name='time_taken',
            field=models.IntegerField(default=0),
        ),
    ]
