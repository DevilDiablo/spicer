# Generated by Django 3.2 on 2021-07-16 06:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0022_auto_20210716_1208'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='machine',
            name='tester',
        ),
        migrations.AddField(
            model_name='assembly',
            name='tester',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='maintenance.tester'),
        ),
    ]
