# Generated by Django 5.1.4 on 2024-12-11 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empl_attendence', '0004_remove_register_id_register_total_days_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empid', models.CharField(max_length=100)),
                ('uploadedat', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]