# Generated by Django 4.0.4 on 2022-05-14 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psg_pharmacy', '0011_alter_messages_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]