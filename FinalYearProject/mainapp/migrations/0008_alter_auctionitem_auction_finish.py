# Generated by Django 4.1.2 on 2022-12-15 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_answer_question_alter_myuser_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionitem',
            name='auction_finish',
            field=models.DateTimeField(),
        ),
    ]
