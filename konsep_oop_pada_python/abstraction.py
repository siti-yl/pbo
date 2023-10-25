#!/usr/bin/env python3

# Copyright (c) Pipin Fitriadi. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license
# information.

from abc import ABC, abstractmethod


class Bentuk(ABC):
    @abstractmethod
    def luas(self):
        return self.__sisi * self.__sisi

    @abstractmethod
    def keliling(self):
        return 4 * self.__sisi


class Persegi(Bentuk):
    def __init__(self, sisi):
        self.__sisi = sisi

    def luas(self):
        return self.__sisi * self.__sisi

    def keliling(self):
        return 4 * self.__sisi


persegi = Persegi(6)
print(persegi.luas())
print(persegi.keliling())
