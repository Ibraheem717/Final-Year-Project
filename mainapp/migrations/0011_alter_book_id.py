# Generated by Django 4.1.2 on 2023-02-12 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0010_alter_booktracker_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='id',
            field=models.CharField(max_length=13, primary_key=True, serialize=False),
        ),
    ]
