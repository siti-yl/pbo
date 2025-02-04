from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.core.exceptions import ValidationError

class Kursus(models.Model):
    judul = models.CharField(max_length=200)
    deskripsi = models.TextField()
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=True)
    instruktur = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.judul


class Siswa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class BiodataSiswa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    siswa = models.OneToOneField(Siswa, on_delete=models.CASCADE, related_name="biodata")
    nama = models.CharField(max_length=100)
    alamat = models.TextField()
    tanggal_lahir = models.DateField(null=True, blank=True)
    nama_orang_tua = models.CharField(max_length=100)
    telepon = models.CharField(max_length=15)
    usia = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.tanggal_lahir:
            today = date.today()
            self.usia = today.year - self.tanggal_lahir.year - ((today.month, today.day) < (self.tanggal_lahir.month, self.tanggal_lahir.day))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Biodata {self.siswa.user.username}"


class Pendaftaran(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    kursus = models.ForeignKey(Kursus, on_delete=models.CASCADE)
    tanggal_daftar = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('siswa', 'kursus')

    def __str__(self):
        return f"Pendaftaran {self.siswa.user.username} ke {self.kursus.judul}"


class Kuis(models.Model):
    kursus = models.ForeignKey(Kursus, on_delete=models.CASCADE)
    pertanyaan = models.TextField()
    jawaban_benar = models.ForeignKey('Pilihan', on_delete=models.SET_NULL, related_name='benar_untuk_kuis', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pertanyaan


class Pilihan(models.Model):
    kuis = models.ForeignKey(Kuis, on_delete=models.CASCADE, related_name='pilihan')
    teks = models.CharField(max_length=200)
    benar = models.BooleanField(default=False)

    def clean(self):
        if self.benar:
            pilihan_benar_count = Pilihan.objects.filter(kuis=self.kuis, benar=True).count()
            if pilihan_benar_count > 1:
                raise ValidationError('Hanya boleh ada satu pilihan benar per soal.')

    def __str__(self):
        return self.teks


class HasilKuis(models.Model):
    FEEDBACK_CHOICES = [
        ('bagus', 'Bagus!'),
        ('coba_lagi', 'Coba lagi.'),
    ]
    
    pendaftaran = models.ForeignKey(Pendaftaran, on_delete=models.CASCADE, related_name='hasil_kuis')
    kuis = models.ForeignKey(Kuis, on_delete=models.CASCADE)
    pilihan = models.ForeignKey('Pilihan', on_delete=models.CASCADE, null=True, blank=True)
    nilai = models.IntegerField(default=0)
    feedback = models.CharField(max_length=10, choices=FEEDBACK_CHOICES, default='coba_lagi')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Hasil Kuis {self.pendaftaran.siswa.user.username} - {self.kuis.pertanyaan}"

    def set_feedback_and_nilai(self):
        if self.pilihan == self.kuis.jawaban_benar:
            self.nilai = 1
            self.feedback = 'bagus'
        else:
            self.nilai = 0
            self.feedback = 'coba_lagi'
        self.save()


class Sertifikat(models.Model):
    pendaftaran = models.OneToOneField(Pendaftaran, on_delete=models.CASCADE)
    tanggal_terbit = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sertifikat {self.pendaftaran.siswa.user.username} - {self.pendaftaran.kursus.judul}"


class Materi(models.Model):
    kursus = models.ForeignKey(Kursus, on_delete=models.CASCADE, related_name='materi')
    judul = models.CharField(max_length=255)
    konten = models.TextField()
    penjelasan = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.judul} - {self.kursus.judul}"

    class Meta:
        ordering = ['created_at']