# Generated by Django 4.0.4 on 2022-05-14 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psg_pharmacy', '0013_alter_messages_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='time',
            field=models.DateField(auto_now_add=True),
        ),
    ]