#!/usr/bin/env python3
# -*- coding: utf-8 -*
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from itertools import tee

__author__ = 'andreas.dahlberg90@gmail.com (Andreas Dahlberg)'
__version__ = '0.1.0'

INPUT_START = 206938
INPUT_END = 679128


def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def is_increasing(password):
    value = int(password[0])
    for c in password[1:]:
        if int(c) < value:
            return False
        value = int(c)
    return True


def get_part_one_answer():
    number_of_passwords = 0

    for i in range(INPUT_START, INPUT_END):
        password = (str(i))

        is_valid = True
        for current_char, next_char in pairwise(password):
            if current_char == next_char:
                if not is_increasing(password):
                    break
                number_of_passwords += 1
                break

    return number_of_passwords


def get_part_two_answer():
    number_of_passwords = 0
    for i in range(INPUT_START, INPUT_END):
        password = (str(i))

        is_valid = True
        for i in range(len(password) - 1):
            if password[i] == password[i + 1]:

                try:
                    if password[i - 1] == password[i]:
                        continue
                except:
                    pass

                try:
                    if password[i + 2] == password[i]:
                        continue
                except:
                    pass

                if not is_increasing(password):
                    break
                number_of_passwords += 1
                break

    return number_of_passwords


def main():
    print('Part 1 answer: {}'.format(get_part_one_answer()))
    print('Part 2 answer: {}'.format(get_part_two_answer()))

    return 0


if __name__ == '__main__':
    exit(main())
