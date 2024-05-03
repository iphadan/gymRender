# Generated by Django 5.0 on 2024-05-03 18:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymManagement', '0007_alter_attendance_workouttime_alter_gymmember_paidat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='workoutDate',
            field=models.DateField(default=datetime.date(2024, 5, 3)),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='workoutTime',
            field=models.TimeField(default=datetime.datetime(2024, 5, 3, 21, 16, 14, 543816)),
        ),
        migrations.AlterField(
            model_name='gymmember',
            name='joinedAt',
            field=models.DateField(default=datetime.date(2024, 5, 3)),
        ),
        migrations.AlterField(
            model_name='gymmember',
            name='paidAt',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 3, 21, 16, 14, 543817)),
        ),
        migrations.AlterField(
            model_name='plan',
            name='createdAt',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 3, 21, 16, 14, 540310)),
        ),
    ]
