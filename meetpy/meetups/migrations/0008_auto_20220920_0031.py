# Generated by Django 3.2.15 on 2022-09-20 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetups', '0007_alter_talkproposal_talk'),
    ]

    operations = [
        migrations.AddField(
            model_name='speaker',
            name='discord_handle',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AddField(
            model_name='speaker',
            name='slack_handle',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]
