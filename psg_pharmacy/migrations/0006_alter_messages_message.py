# Generated by Django 4.0.4 on 2022-05-14 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psg_pharmacy', '0005_alter_mail_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='message',
            field=models.CharField(max_length=1000),
        ),
    ]
