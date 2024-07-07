# Generated by Django 5.0.6 on 2024-07-06 09:08

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='description',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='orgId',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]