# Generated by Django 4.1.2 on 2022-12-12 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_auctionitem_rename_dateofbirth_myuser_date_of_birth_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionitem',
            name='item_picture',
            field=models.ImageField(default='defaultIcon.jpg', upload_to='items/'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='profile_picture',
            field=models.ImageField(default='defaultIcon.jpg', upload_to='users/'),
        ),
    ]