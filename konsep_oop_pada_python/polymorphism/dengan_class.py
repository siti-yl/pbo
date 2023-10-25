#!/usr/bin/env python3

# Copyright (c) Pipin Fitriadi. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license
# information.

class Kucing:
    def __init__(self, nama, umur):
        self.nama = nama
        self.umur = umur

    def bersuara(self):
        print('Meow')


class Dog:
    def __init__(self, nama, umur):
        self.nama = nama
        self.umur = umur

    def bersuara(self):
        print('Guk..guk...')


kucing1 = Kucing('Tom', 3)
anjing1 = Dog('Spike', 4)

for hewan in (kucing1, anjing1):
    hewan.bersuara()
