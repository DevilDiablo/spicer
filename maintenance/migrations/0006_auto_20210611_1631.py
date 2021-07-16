# Generated by Django 3.2 on 2021-06-11 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0005_standard_range_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='standard_binary',
            name='frequency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='maintenance.frequency'),
        ),
        migrations.AddField(
            model_name='standard_range',
            name='frequency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='maintenance.frequency'),
        ),
        migrations.AddField(
            model_name='standard_value',
            name='frequency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='maintenance.frequency'),
        ),
    ]
