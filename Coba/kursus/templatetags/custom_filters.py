from django import template
from kursus.models import Pilihan

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Mengambil nilai dari dictionary berdasarkan key."""
    if isinstance(dictionary, dict):
        return dictionary.get(key, None)
    return None

@register.filter
def is_correct(jawaban_id, kuis_id):
    """Memeriksa apakah jawaban pengguna benar."""
    try:
        jawaban_pengguna = Pilihan.objects.get(id=jawaban_id)
        jawaban_benar = Pilihan.objects.get(kuis=jawaban_pengguna.kuis, benar=True)

        return jawaban_pengguna.id == jawaban_benar.id
    except (Pilihan.DoesNotExist, Pilihan.MultipleObjectsReturned):
        return False

@register.filter
def split_lines(value):
    """Filter untuk membagi string berdasarkan baris baru."""
    if isinstance(value, str): 
        return value.split('\n')
    return value
