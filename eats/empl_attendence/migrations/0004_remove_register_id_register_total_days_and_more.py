# Generated by Django 5.1.4 on 2024-12-11 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empl_attendence', '0003_alter_register_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='register',
            name='id',
        ),
        migrations.AddField(
            model_name='register',
            name='total_days',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='register',
            name='emp_email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='register',
            name='empid',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='register',
            name='phone_number',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
