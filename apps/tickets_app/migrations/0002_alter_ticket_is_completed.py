# Generated by Django 3.2.6 on 2021-09-19 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='is_completed',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]