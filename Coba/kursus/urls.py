from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_redirect, name='home_redirect'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('daftar_kursus/', views.daftar_kursus, name='daftar_kursus'),
    path('biodata/', views.biodata_view, name='biodata'),
    path('siswa/', views.halaman_siswa, name='halaman_siswa'),
    path('kuis/', views.halaman_kuis, name='kuis'),
    path('hasil_kuis/<int:pendaftaran_id>/', views.hasil_kuis, name='hasil_kuis'),
    path('hasil_kuis/', views.hasil_kuis_redirect, name='hasil_kuis_redirect'),
    path('materi/', views.materi_view, name='materi'),
    path('materi/<int:kursus_id>/', views.materi_view, name='materi_view'),
    path('materi/detail/<int:materi_id>/', views.materi_detail, name='materi_detail'),
    path('mendaftar/<int:kursus_id>/', views.mendaftar_kursus, name='mendaftar_kursus'),
    path('sertifikat/<int:pendaftaran_id>/', views.lihat_sertifikat, name='lihat_sertifikat'),
    path('buat_siswa/', views.buat_siswa, name='buat_siswa'),
    path('kuis/<int:kursus_id>/', views.kuis_view, name='kuis'),
    path('logout/', views.logout_view, name='logout'),
]
