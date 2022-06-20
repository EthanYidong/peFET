# Generated by Django 4.0.5 on 2022-06-20 05:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_participant_last_email_sent'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedFetImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploads/fet/')),
                ('participant', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='api.participant')),
            ],
        ),
    ]
