# Generated by Django 5.1.5 on 2025-02-02 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kursus', '0007_remove_hasilkuis_jawaban_alter_kuis_jawaban_benar_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='pendaftaran',
            unique_together={('siswa', 'kursus')},
        ),
    ]
