# Generated by Django 5.0.6 on 2024-07-06 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('orgId', models.UUIDField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=500, null=True)),
            ],
        ),
    ]