# Generated by Django 3.0.7 on 2020-11-08 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0004_auto_20201108_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='epigone',
            field=models.BooleanField(default=False, help_text='Czy podmiot ma osobną listę piosenek epigońskich.'),
        ),
        migrations.AddField(
            model_name='song',
            name='epigone',
            field=models.BooleanField(default=False, help_text='Czy piosenka jest kompozycją epigońską, bez porozumienia z autorem tekstu.'),
        ),
    ]
