# Generated by Django 4.0.1 on 2022-03-14 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hours', '0002_user_bio_user_name_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='avatar.svg', null=True, upload_to=''),
        ),
    ]