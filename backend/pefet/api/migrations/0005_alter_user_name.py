# Generated by Django 4.0.5 on 2022-06-15 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_user_id_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(default='AnonymousUser', max_length=100),
        ),
    ]