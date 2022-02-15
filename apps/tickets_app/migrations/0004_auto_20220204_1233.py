# Generated by Django 3.2.6 on 2022-02-04 12:33

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('tickets_app', '0003_ticket_section'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraField',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=252, null=True)),
                ('value', models.CharField(blank=True, max_length=252, null=True)),
                ('type', models.CharField(blank=True, max_length=252, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='taskpriority',
            name='options',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='priority',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='status',
        ),
        migrations.RenameModel(
            old_name='TaskPriorityOptions',
            new_name='ExtraFieldptions',
        ),
        migrations.DeleteModel(
            name='Status',
        ),
        migrations.DeleteModel(
            name='StatusOptions',
        ),
        migrations.DeleteModel(
            name='TaskPriority',
        ),
        migrations.AddField(
            model_name='extrafield',
            name='options',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tickets_app.extrafieldptions'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='extra_field',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tickets_app.extrafield'),
        ),
    ]