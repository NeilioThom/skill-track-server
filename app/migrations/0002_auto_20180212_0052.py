# Generated by Django 2.0.2 on 2018-02-12 00:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='timeentry',
            options={'verbose_name_plural': 'Time Entries'},
        ),
        migrations.AlterField(
            model_name='timeentry',
            name='skill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='app.Skill'),
        ),
    ]