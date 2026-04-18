from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('udltimes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='statsframed',
            name='points',
            field=models.IntegerField(default=0),
        ),
    ]