# Generated by Django 3.2.15 on 2022-09-20 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetups', '0009_add_though_for_sponsors'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meetupsponsorthrough',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='meetupsponsorthrough',
            name='order',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
