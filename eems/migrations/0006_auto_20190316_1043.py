# Generated by Django 2.0.2 on 2019-03-16 01:43

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('eems', '0005_auto_20190311_2314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='current_entry',
            name='entry_time',
        ),
        migrations.RemoveField(
            model_name='current_entry',
            name='leave_time',
        ),
        migrations.RemoveField(
            model_name='current_entry',
            name='line_id',
        ),
        migrations.RemoveField(
            model_name='current_entry',
            name='line_name',
        ),
        migrations.RemoveField(
            model_name='current_entry',
            name='user_img',
        ),
        migrations.AddField(
            model_name='current_entry',
            name='user_info',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='eems.User_Master'),
        ),
        migrations.AddField(
            model_name='user_master',
            name='entry_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='user_master',
            name='leave_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='user_master',
            name='company',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AlterField(
            model_name='user_master',
            name='department',
            field=models.CharField(default='', max_length=128),
        ),
    ]
