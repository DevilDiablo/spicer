# Generated by Django 3.2 on 2021-06-24 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0014_auto_20210623_2227'),
    ]

    operations = [
        migrations.AddField(
            model_name='standard',
            name='time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
