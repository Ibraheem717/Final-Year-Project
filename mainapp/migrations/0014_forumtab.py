# Generated by Django 4.1.2 on 2023-02-14 10:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0013_myuser_private'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForumTab',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=54)),
                ('forum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.forum')),
            ],
        ),
    ]
