# Generated by Django 4.2.7 on 2024-01-19 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tuition', '0006_rename_subject_tuition_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='applytuition',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tuition.tuitionsubject'),
        ),
    ]
