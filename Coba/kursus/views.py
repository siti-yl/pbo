from django.shortcuts import render, redirect, get_object_or_404
from .models import Kursus, Pendaftaran, HasilKuis, Sertifikat, Siswa, BiodataSiswa, Pilihan, Materi
from .forms import PendaftaranForm, HasilKuisForm, BiodataForm 
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def home_redirect(request):
    if request.user.is_authenticated:
        print(f"User {request.user.username} sudah login.")
        return redirect('daftar_kursus')
    else:
        print("User belum login.")
        return redirect('login')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('daftar_kursus')
        else:
            messages.error(request, 'Username atau password salah.')

    return render(request, 'login.html')

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username sudah digunakan.')
        else:
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                messages.success(request, 'Pendaftaran berhasil! Silakan login.')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Terjadi kesalahan: {str(e)}')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def daftar_kursus(request):
    kursus_list = Kursus.objects.all()

    try:
        siswa = request.user.siswa
        pendaftaran_list = Pendaftaran.objects.filter(siswa=siswa)
    except Siswa.DoesNotExist:
        messages.error(request, "Anda harus mengisi biodata terlebih dahulu.")
        return redirect('buat_siswa')

    return render(request, 'daftar_kursus.html', {
        'kursus_list': kursus_list,
        'pendaftaran_list': pendaftaran_list,
    })

@login_required
def mendaftar_kursus(request, kursus_id):
    kursus = get_object_or_404(Kursus, id=kursus_id)

    if not kursus.status:
        messages.error(request, 'Kursus sudah ditutup.')
        return redirect('daftar_kursus')

    try:
        siswa = request.user.siswa
    except Siswa.DoesNotExist:
        messages.error(request, "Anda perlu mendaftar sebagai siswa terlebih dahulu.")
        return redirect('buat_siswa')

    if Pendaftaran.objects.filter(siswa=siswa, kursus=kursus).exists():
        messages.warning(request, "Anda sudah terdaftar di kursus ini.")
        return redirect('halaman_siswa')

    if request.method == 'POST':
        pendaftaran = Pendaftaran(siswa=siswa, kursus=kursus)
        pendaftaran.save()
        messages.success(request, "Pendaftaran kursus berhasil!")
        return redirect('halaman_siswa')
    
    return render(request, 'mendaftar_kursus.html', {'kursus': kursus})


@login_required
def buat_siswa(request):
    try:
        if hasattr(request.user, 'siswa'):
            return redirect('daftar_kursus')

        if request.method == "POST":
            form = BiodataForm(request.POST)
            if form.is_valid():
                siswa = form.save(commit=False)
                siswa.user = request.user
                siswa.save()
                messages.success(request, "Biodata berhasil disimpan! Silakan pilih kursus.")
                return redirect('daftar_kursus')
        else:
            form = BiodataForm()

        return render(request, 'buat_siswa.html', {'form': form})

    except Exception as e:
        messages.error(request, f"Terjadi kesalahan: {e}")
        return redirect('halaman_login')


@login_required
def buat_siswa(request):
    if hasattr(request.user, 'siswa'):
        return redirect('daftar_kursus')

    if request.method == "POST":
        form = BiodataForm(request.POST)
        if form.is_valid():
            siswa = form.save(commit=False)
            siswa.user = request.user
            siswa.save()
            messages.success(request, "Biodata berhasil disimpan! Silakan pilih kursus.")
            return redirect('daftar_kursus')
    else:
        form = BiodataForm()

    return render(request, 'biodata.html', {'form': form})

@login_required
def biodata_view(request):

    siswa, created = Siswa.objects.get_or_create(user=request.user)

    biodata, created = BiodataSiswa.objects.get_or_create(siswa=siswa)

    if request.method == 'POST':
        form = BiodataForm(request.POST, instance=biodata)
        if form.is_valid():
            biodata = form.save(commit=False)
            biodata.siswa = siswa
            biodata.save()
            messages.success(request, 'Biodata berhasil disimpan!')
            return redirect('daftar_kursus')
    else:
        form = BiodataForm(instance=biodata)

    return render(request, 'biodata.html', {'form': form})


@login_required
def hasil_kuis(request, pendaftaran_id):
    pendaftaran = get_object_or_404(Pendaftaran, id=pendaftaran_id)

    if not Pendaftaran.objects.filter(siswa=request.user.siswa, kursus=pendaftaran.kursus).exists():
        messages.error(request, "Anda harus mendaftar terlebih dahulu untuk melihat hasil kuis.")
        return redirect('daftar_kursus')

    kuis = pendaftaran.kursus.kuis_set.all()
    hasil_kuis_list = HasilKuis.objects.filter(pendaftaran=pendaftaran)

    if not hasil_kuis_list.exists():
        messages.warning(request, "Anda belum mengerjakan kuis ini.")
        return redirect('kerjakan_kuis', pendaftaran_id=pendaftaran.id)

    nilai_total = sum(hk.nilai for hk in hasil_kuis_list)
    total_soal = kuis.count()

    if nilai_total == total_soal:
        sertifikat, created = Sertifikat.objects.get_or_create(pendaftaran=pendaftaran)
        if created:
            messages.success(request, "Selamat! Anda telah mendapatkan sertifikat.")

    return render(request, 'kursus/hasil_kuis.html', {
        'pendaftaran': pendaftaran,
        'hasil_kuis_list': hasil_kuis_list,
        'nilai_total': nilai_total,
        'total_soal': total_soal,
        'sertifikat': Sertifikat.objects.filter(pendaftaran=pendaftaran).first()
    })


@login_required
def lihat_sertifikat(request, pendaftaran_id):
    sertifikat = get_object_or_404(Sertifikat, pendaftaran_id=pendaftaran_id)
    return render(request, 'lihat_sertifikat.html', {'sertifikat': sertifikat})

@login_required
def halaman_siswa(request):
    pendaftarans = Pendaftaran.objects.filter(siswa=request.user.siswa)
    kursus_list = [pendaftaran.kursus for pendaftaran in pendaftarans]
    return render(request, 'siswa.html', {'kursus': kursus_list})

@login_required
def kuis_view(request, kursus_id):
    kursus = get_object_or_404(Kursus, id=kursus_id)
    kuis = kursus.kuis_set.all()

    pendaftaran = Pendaftaran.objects.filter(siswa=request.user.siswa, kursus=kursus).first()
    if not pendaftaran:
        messages.error(request, "Anda harus mendaftar terlebih dahulu untuk mengikuti kuis.")
        return redirect('daftar_kursus')

    if request.method == 'POST':
        jawaban = {}
        error_message = None
        nilai_total = 0
        hasil_kuis_dict = {}

        for kuis_item in kuis:
            jawaban_id = request.POST.get(f'jawaban_{kuis_item.id}')
            if not jawaban_id:
                error_message = f"Soal '{kuis_item.pertanyaan}' harus dijawab."
                break

            pilihan = Pilihan.objects.filter(id=jawaban_id).first()
            if not pilihan:
                error_message = f"Jawaban tidak valid untuk soal '{kuis_item.pertanyaan}'."
                break

            is_benar = pilihan.benar
            feedback = 'Jawaban Anda Benar' if is_benar else f'Jawaban Anda Salah. Jawaban yang benar: {kuis_item.jawaban_benar.teks}'

            nilai = 1 if is_benar else 0
            nilai_total += nilai

            HasilKuis.objects.create(
                pendaftaran=pendaftaran,
                kuis=kuis_item,
                pilihan=pilihan,
                nilai=nilai
            )

            hasil_kuis_dict[kuis_item.id] = {
                'jawaban_dipilih': pilihan.teks,
                'benar': is_benar,
                'feedback': feedback
            }

        if error_message:
            return render(request, 'kuis.html', {
                'kursus': kursus, 'kuis': kuis, 'pendaftaran': pendaftaran, 'error_message': error_message
            })

    
        messages.success(request, f"Kuis selesai! Nilai Anda: {nilai_total}/{kuis.count()}.")
        return render(request, 'kursus/hasil_kuis.html', {'nilai_total': nilai_total, 'kuis_count': kuis.count(), 'hasil_kuis': hasil_kuis})

    return render(request, 'kuis.html', {'kursus': kursus, 'kuis': kuis, 'pendaftaran': pendaftaran})

def materi_view(request, kursus_id=None):
    if kursus_id:
        kursus = get_object_or_404(Kursus, id=kursus_id)
        materi = Materi.objects.filter(kursus=kursus)
    else:
        kursus = None
        materi = Materi.objects.all()

    print("Jumlah Materi:", materi.count())
    for m in materi:
        print(m.judul)

    return render(request, 'materi.html', {
        'kursus': kursus,
        'materi': materi,
    })


@login_required
def halaman_kuis(request):
    if request.method == 'POST':
        pendaftaran_id = request.POST.get('pendaftaran_id')
        kursus = request.POST.get('kursus')

        if pendaftaran_id and kursus:
            pendaftaran = get_object_or_404(Pendaftaran, id=pendaftaran_id)
            return redirect('hasil_kuis', pendaftaran_id=pendaftaran.id)
        else:
            messages.error(request, 'Terjadi kesalahan. Silakan pilih kursus dan coba lagi.')
            return redirect('daftar_kursus')
    return redirect('daftar_kursus')


def halaman_materi(request):
    return render(request, "materi.html")

def get_pilihan():
    from .models import Pilihan
    return Pilihan.objects.all()

def hasil_kuis_redirect(request):
    pendaftaran = Pendaftaran.objects.filter(siswa=request.user.siswa).first()
    
    if not pendaftaran:
        messages.error(request, "Anda belum mendaftar untuk kuis ini.")
        return redirect('daftar_kursus')

    return redirect('hasil_kuis', pendaftaran_id=pendaftaran.id)

def materi_detail(request, materi_id):
    materi = get_object_or_404(Materi, id=materi_id)
    
    kursus = materi.kursus  
    
    return render(request, 'materi_detail.html', {
        'materi': materi,
        'kursus': kursus,
    })