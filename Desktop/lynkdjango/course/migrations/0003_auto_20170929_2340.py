# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-30 06:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_auto_20170929_2113'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='grade_threshold_A',
            field=models.DecimalField(decimal_places=2, default=0.93, max_digits=5),
        ),
        migrations.AddField(
            model_name='course',
            name='grade_threshold_A_minus',
            field=models.DecimalField(decimal_places=2, default=0.9, max_digits=5),
        ),
        migrations.AddField(
            model_name='course',
            name='grade_threshold_A_plus',
            field=models.DecimalField(decimal_places=2, default=0.97, max_digits=5),
        ),
        migrations.AddField(
            model_name='course',
            name='grade_threshold_B',
            field=models.DecimalField(decimal_places=2, default=0.83, max_digits=5),
        ),
        migrations.AddField(
            model_name='course',
            name='grade_threshold_B_minus',
            field=models.DecimalField(decimal_places=2, default=0.8, max_digits=5),
        ),
        migrations.AddField(
            model_name='course',
            name='grade_threshold_B_plus',
            field=models.DecimalField(decimal_places=2, default=0.87, max_digits=5),
        ),
        migrations.AddField(
            model_name='course',
            name='grade_threshold_C',
            field=models.DecimalField(decimal_places=2, default=0.73, max_digits=5),
        ),
        migrations.AddField(
            model_name='course',
            name='grade_threshold_C_minus',
            field=models.DecimalField(decimal_places=2, default=0.7, max_digits=5),
        ),
        migrations.AddField(
            model_name='course',
            name='grade_threshold_C_plus',
            field=models.DecimalField(decimal_places=2, default=0.77, max_digits=5),
        ),
        migrations.AddField(
            model_name='course',
            name='grade_threshold_D',
            field=models.DecimalField(decimal_places=2, default=0.63, max_digits=5),
        ),
        migrations.AddField(
            model_name='course',
            name='grade_threshold_D_minus',
            field=models.DecimalField(decimal_places=2, default=0.6, max_digits=5),
        ),
        migrations.AddField(
            model_name='course',
            name='grade_threshold_D_plus',
            field=models.DecimalField(decimal_places=2, default=0.67, max_digits=5),
        ),
        migrations.AddField(
            model_name='course',
            name='grade_threshold_F',
            field=models.DecimalField(decimal_places=2, default=0.53, max_digits=5),
        ),
        migrations.AddField(
            model_name='course',
            name='grade_threshold_F_minus',
            field=models.DecimalField(decimal_places=2, default=0.5, max_digits=5),
        ),
        migrations.AddField(
            model_name='course',
            name='grade_threshold_F_plus',
            field=models.DecimalField(decimal_places=2, default=0.57, max_digits=5),
        ),
        migrations.AddField(
            model_name='course',
            name='passing_grade',
            field=models.DecimalField(decimal_places=2, default=0.7, max_digits=5),
        ),
        migrations.AlterField(
            model_name='course',
            name='calendar_link',
            field=models.CharField(default='', max_length=256),
        ),
    ]
