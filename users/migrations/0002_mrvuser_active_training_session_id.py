# Generated by Django 4.2.2 on 2023-06-19 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mrvuser',
            name='active_training_session_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
