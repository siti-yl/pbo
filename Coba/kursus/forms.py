from django import forms
from .models import Pendaftaran, HasilKuis, BiodataSiswa

class PendaftaranForm(forms.ModelForm):
    class Meta:
        model = Pendaftaran
        fields = ['kursus']

class HasilKuisForm(forms.ModelForm):
    class Meta:
        model = HasilKuis
        fields = ['pendaftaran', 'kuis', 'pilihan', 'nilai', 'feedback']

class BiodataForm(forms.ModelForm):
    class Meta:
        model = BiodataSiswa
        fields = ['nama', 'alamat', 'tanggal_lahir', 'nama_orang_tua', 'telepon']
        widgets = {
            'tanggal_lahir': forms.DateInput(attrs={'type': 'date'}),
        }
