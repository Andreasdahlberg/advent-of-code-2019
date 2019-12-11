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

__author__ = 'andreas.dahlberg90@gmail.com (Andreas Dahlberg)'
__version__ = '0.1.0'


from itertools import permutations

from aoc.int_code_computer import *



def main():


    int_code = get_int_code_from_file('input.txt')


    outputs = []

    phase_settings = permutations(range(5))
    for phase_setting in phase_settings:
        print('New phase setting:', phase_setting)


        input_signal = 0
        for i in range(5):
            print('Amplifier stage:', i)
            computer = IntCodeComputer(int_code)
            computer.input(phase_setting[i])
            computer.input(input_signal)
            computer.execute()

            input_signal = computer.outputs[-1]

        outputs.append(input_signal)
    print(outputs)


    print('Part 1 answer: {}'.format(max(outputs)))
    print('Part 2 answer: {}'.format(None))

    return 0


if __name__ == '__main__':
    exit(main())
