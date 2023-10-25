#!/usr/bin/env python3

# Copyright (c) Pipin Fitriadi. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license
# information.

class Halo:
    def __init__(self, angka):
        # Public attribute
        self.a = 123

        # Private attribute dapat diakses class turunan dan instance
        self._b = 20

        # Private attribute tidak dapat diakses class turunan dan instance
        self.__c = 40


class Software:
    # Instance attribute
    def __init__(self):
        # Private attribute tidak dapat diakses class turunan dan instance
        self.__version = 1

    # Instance method
    def get_version(self):
        print(self.__version)

    def set_version(self, version):
        self.__version = version


# Instanstiate objek Software
obj = Software()
obj.get_version()
obj.set_version(3)
obj.get_version()


halo = Halo('angka')
print(halo.a)
print(halo._b)
print(halo.__c)  # Akan error karena tidak dapat diakses oleh instance
