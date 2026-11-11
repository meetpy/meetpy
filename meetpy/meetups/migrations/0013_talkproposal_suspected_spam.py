from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetups', '0012_add_meetup_video_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='talkproposal',
            name='suspected_spam',
            field=models.BooleanField(default=False),
        ),
    ]
