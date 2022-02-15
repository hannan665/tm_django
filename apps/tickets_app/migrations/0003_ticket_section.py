# Generated by Django 3.2.6 on 2021-09-19 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task_section_app', '0002_alter_section_project'),
        ('tickets_app', '0002_alter_ticket_is_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='task_section_app.section'),
        ),
    ]
