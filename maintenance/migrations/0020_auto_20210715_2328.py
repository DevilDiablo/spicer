# Generated by Django 3.2 on 2021-07-15 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0019_auto_20210715_1725'),
    ]

    operations = [
        migrations.AddField(
            model_name='standard_binary',
            name='approved',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='standard_range',
            name='approved',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='standard_ryb',
            name='approved',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='standard_ryb',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='rybimg/'),
        ),
        migrations.AddField(
            model_name='standard_value',
            name='approved',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]