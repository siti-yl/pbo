#!/usr/bin/env python3

# Copyright (c) Pipin Fitriadi. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license
# information.

class Burung:
    def intro(self):
        print('Di dunia ini ada beberapa type berbeda dari spesies burung')

    def terbang(self):
        print(
            'Hampir semua burung dapat terbang, namun ada beberapa yang tidak '
            'dapat terbang'
        )


class Elang(Burung):
    def terbang(self):
        print('Elang dapat terbang')


class BurungUnta(Burung):
    def terbang(self):
        print('Burung unta tidak dapat terbang')


obj_burung = Burung()
obj_elang = Elang()
obj_burung_unta = BurungUnta()

for burung in (obj_burung, obj_elang, obj_burung_unta):
    burung.intro()
    burung.terbang()
