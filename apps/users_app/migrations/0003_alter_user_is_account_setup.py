# Generated by Django 3.2.6 on 2021-09-02 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0002_auto_20210902_0846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_account_setup',
            field=models.BooleanField(default=False, verbose_name='Is account setup?'),
        ),
    ]
