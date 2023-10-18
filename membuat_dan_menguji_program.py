from datetime import date


class Barang:
    jumlah: int  # contoh deklarasi
    harga_beli: int
    tanggal_kadaluwarsa: date
    harga_jual: int
    id_barang: str
    diskon: float = 0.0  # contoh penugasan

    def set_id_barang(self, id: str):
        self.id_barang = id


if __name__ == '__main__':
    # Barang().jumlah = 3
    print(Barang().diskon)

    b = Barang()
    print(b)
    b.jumlah = 3
    print(b.jumlah)
    print(b.diskon)
    b.diskon = 5/2
    print(b.diskon)
    b.set_id_barang(id='a')
    print(b.id_barang)
    b.set_id_barang('b')
    print(b.id_barang)
