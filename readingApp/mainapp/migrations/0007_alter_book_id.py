# Generated by Django 4.1.2 on 2023-02-05 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_authormessages_id_bookmessages_id_forummessages_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='id',
            field=models.IntegerField(max_length=13, primary_key=True, serialize=False),
        ),
    ]
