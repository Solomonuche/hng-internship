# Generated by Django 5.0.6 on 2024-07-06 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0003_alter_organisation_description_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='organisation',
            old_name='user',
            new_name='users',
        ),
    ]
