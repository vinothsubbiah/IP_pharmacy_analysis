# Generated by Django 4.0.4 on 2022-05-14 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psg_pharmacy', '0007_alter_mail_time_alter_messages_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='messages',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]