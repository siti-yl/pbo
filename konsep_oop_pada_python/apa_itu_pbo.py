#!/usr/bin/env python3

# Copyright (c) Pipin Fitriadi. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license
# information.

class Mobil:
    def __init__(self, tipe=None, roda=None, kecepatan=0):
        self.tipe = tipe
        self.roda = roda
        self.kecepatan = kecepatan

    def do_melaju(self):
        print('Melaju dengan kecepatan:', self.kecepatan, 'km/h')

    def do_klakson(self):
        print('Klakson')

    def do_belok(self, arah):
        print('Belok arah', arah)


class Karyawan:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduction(self):
        print(f'Hallo, nama saya {self.name}. Umur saya {self.age}.')

    def work(self):
        print('Mari Kita Kerja!')


mobil_ferrari = Mobil('Sport', 4, 200)
print(mobil_ferrari.tipe)
mobil_ferrari.do_melaju()

mobil_jeep = Mobil('Offroad', 6, 150)
print(mobil_jeep.tipe)
mobil_jeep.do_melaju()

karyawan1 = Karyawan('Aqshol', 19)
karyawan1.introduction()
karyawan1.work()

karyawan2 = Karyawan('Hamid', 21)
karyawan2.introduction()
karyawan2.work()
