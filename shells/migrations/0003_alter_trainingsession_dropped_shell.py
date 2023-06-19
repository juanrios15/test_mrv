# Generated by Django 4.2.2 on 2023-06-18 22:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shells', '0002_remove_trainingsession_candidate_shells_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainingsession',
            name='dropped_shell',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dropped_shell', to='shells.shell'),
        ),
    ]