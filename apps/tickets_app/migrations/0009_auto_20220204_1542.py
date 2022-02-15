# Generated by Django 3.2.6 on 2022-02-04 15:42

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('tickets_app', '0008_alter_extrafield_ticket'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraFieldOptions',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=250, null=True)),
                ('color', models.CharField(blank=True, max_length=250, null=True)),
                ('extra_field', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='options', to='tickets_app.extrafield')),
            ],
        ),
        migrations.DeleteModel(
            name='ExtraFieldptions',
        ),
    ]