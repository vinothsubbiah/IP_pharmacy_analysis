# Generated by Django 4.0.4 on 2022-05-14 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psg_pharmacy', '0016_alter_mail_time_alter_messages_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='current_quantity',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='messages',
            name='demand',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='messages',
            name='drug_code',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='messages',
            name='proposed_order_quantity',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
