# Generated by Django 4.0.4 on 2022-05-09 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('psg_pharmacy', '0003_mail'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mail',
            old_name='message',
            new_name='body',
        ),
    ]
