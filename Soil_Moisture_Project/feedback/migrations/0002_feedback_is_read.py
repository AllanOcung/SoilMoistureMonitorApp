# Generated by Django 5.0.7 on 2024-07-26 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]