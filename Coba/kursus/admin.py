from django.contrib import admin
from .models import Kursus, Siswa, BiodataSiswa, Pendaftaran, Kuis, Pilihan, HasilKuis, Sertifikat,Materi

admin.site.register(Kursus)
admin.site.register(Siswa)
admin.site.register(BiodataSiswa)
admin.site.register(Pendaftaran)
admin.site.register(Kuis)
admin.site.register(Pilihan)
admin.site.register(HasilKuis)
admin.site.register(Sertifikat)

@admin.register(Materi)
class MateriAdmin(admin.ModelAdmin):
    list_display = ('judul', 'kursus', 'created_at')
    search_fields = ('judul', 'konten')