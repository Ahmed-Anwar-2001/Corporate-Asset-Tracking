# Generated by Django 5.0.5 on 2024-05-09 13:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corporate_assets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='corporate_assets.branch'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='corporate_assets.company'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='designation',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='joining_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='nationality',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
