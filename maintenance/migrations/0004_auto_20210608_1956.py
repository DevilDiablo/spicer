# Generated by Django 3.2 on 2021-06-08 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0003_standard_range_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='standard_binary',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='stanbinary/'),
        ),
        migrations.AddField(
            model_name='standard_range',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='stanrange/'),
        ),
        migrations.AddField(
            model_name='standard_value',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='stanvalue/'),
        ),
        migrations.AddField(
            model_name='standard_value',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
