# Generated by Django 4.2.7 on 2024-01-24 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_tuitionreview'),
    ]

    operations = [
        migrations.AddField(
            model_name='tuitionreview',
            name='teacher_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
