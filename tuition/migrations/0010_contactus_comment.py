# Generated by Django 4.2.7 on 2024-01-25 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tuition', '0009_contactus'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactus',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]