# Generated by Django 2.0.2 on 2018-02-12 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_skill_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='created_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
