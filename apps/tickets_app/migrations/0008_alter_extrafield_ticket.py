# Generated by Django 3.2.6 on 2022-02-04 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets_app', '0007_auto_20220204_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extrafield',
            name='ticket',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='extra_fields', to='tickets_app.ticket'),
        ),
    ]