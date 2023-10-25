#!/usr/bin/env python3

# Copyright (c) Pipin Fitriadi. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license
# information.

# Parent 1
class Perhitungan1:
    def penjumlahan(self, a, b):
        return a + b


# Parent 2
class Perhitungan2:
    def perkalian(self, a, b):
        return a * b


# Child
class Child(Perhitungan1, Perhitungan2):
    def pembagian(self, a, b):
        return a / b


c = Child()

print(c.penjumlahan(20, 30))
print(c.perkalian(5, 4))
print(c.pembagian(6, 12))
