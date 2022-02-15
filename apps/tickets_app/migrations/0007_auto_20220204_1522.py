# Generated by Django 3.2.6 on 2022-02-04 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tickets_app', '0006_alter_ticket_extra_field'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extrafield',
            name='options',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='extra_field',
        ),
        migrations.AddField(
            model_name='extrafield',
            name='ticket',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tickets_app.ticket'),
        ),
        migrations.AddField(
            model_name='extrafieldptions',
            name='extra_field',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tickets_app.extrafield'),
        ),
    ]
