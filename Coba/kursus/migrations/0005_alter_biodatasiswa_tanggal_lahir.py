# Generated by Django 5.1.5 on 2025-02-02 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kursus', '0004_remove_siswa_created_at_remove_siswa_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biodatasiswa',
            name='tanggal_lahir',
            field=models.DateField(blank=True, null=True),
        ),
    ]
