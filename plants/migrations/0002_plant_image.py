# Generated by Django 4.2.5 on 2023-10-19 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plants', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant',
            name='image',
            field=models.TextField(null=True),
        ),
    ]