# Generated by Django 2.0.2 on 2018-02-12 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_skill_created_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeentry',
            name='comment',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
    ]