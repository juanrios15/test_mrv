# Generated by Django 4.2.2 on 2023-06-19 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shells', '0004_alter_usershell_difficulty_evaluation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainingsession',
            name='finished_time',
            field=models.DateField(blank=True, null=True),
        ),
    ]