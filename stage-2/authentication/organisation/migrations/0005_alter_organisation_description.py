# Generated by Django 5.0.6 on 2024-07-07 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0004_rename_user_organisation_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='description',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
    ]