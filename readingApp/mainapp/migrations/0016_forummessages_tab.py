# Generated by Django 4.1.2 on 2023-02-14 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0015_rename_author_id_authormessages_author_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='forummessages',
            name='tab',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.forumtab'),
        ),
    ]
