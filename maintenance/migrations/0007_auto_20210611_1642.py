# Generated by Django 3.2 on 2021-06-11 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0006_auto_20210611_1631'),
    ]

    operations = [
        migrations.CreateModel(
            name='range_value',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lower_limit', models.BooleanField(blank=True, default=False, null=True)),
                ('upper_limit', models.BooleanField(blank=True, default=False, null=True)),
                ('less_than', models.IntegerField(blank=True, null=True)),
                ('more_than', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='standard_range',
            name='less_than',
        ),
        migrations.RemoveField(
            model_name='standard_range',
            name='lower_limit',
        ),
        migrations.RemoveField(
            model_name='standard_range',
            name='more_than',
        ),
        migrations.RemoveField(
            model_name='standard_range',
            name='upper_limit',
        ),
    ]