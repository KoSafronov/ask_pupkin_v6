# Generated by Django 5.0.6 on 2024-06-16 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='/uploads/avatars/empty/inkognito.jpg', null=True, upload_to='uploads/avatars/'),
        ),
    ]
