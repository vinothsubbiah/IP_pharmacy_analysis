# Generated by Django 4.0.3 on 2022-05-09 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psg_pharmacy', '0004_rename_message_mail_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='body',
            field=models.TextField(max_length=2000),
        ),
    ]
