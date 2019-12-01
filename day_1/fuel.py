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


def get_input_from_file(file_name):
    """Get all modules from the given file."""
    modules = []

    with open(file_name) as file:
        lines = file.readlines()

        for line in lines:
            modules.append(int(line.strip()))

    return modules


def calculate_required_fuel_for_mass(mass):
    return int(mass / 3) - 2


def calculate_required_fuel_for_module(module_mass):
    total_fuel = 0
    mass = module_mass

    while True:
        fuel = calculate_required_fuel_for_mass(mass)
        if fuel > 0:
            total_fuel += fuel
            mass = fuel
        else:
            break

    return total_fuel


def get_part_one_answer(modules):
    required_fuel = 0
    for mass in modules:
        required_fuel += calculate_required_fuel_for_mass(mass)
    return required_fuel


def get_part_two_answer(modules):
    required_fuel = 0
    for mass in modules:
        required_fuel += calculate_required_fuel_for_module(mass)
    return required_fuel


def main():
    modules = get_input_from_file('input.txt')

    print('Part 1 answer: {}'.format(get_part_one_answer(modules)))
    print('Part 2 answer: {}'.format(get_part_two_answer(modules)))
    return 0

if __name__ == '__main__':
    exit(main())
