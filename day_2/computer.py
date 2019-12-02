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

from collections import namedtuple

Instruction = namedtuple('Instruction', ['opcode', 'a',  'b', 'c'])


def get_integers_from_file(file_name):
    """Get all integers from the given file."""
    integers = []

    with open(file_name) as file:
        lines = file.readlines()

        for line in lines:
            integers.extend([int(integer) for integer in line.rstrip().split(',')])

    return integers


def add(instruction, registers):
    registers[instruction.c] = registers[instruction.a] + registers[instruction.b]
    return True


def multi(instruction, registers):
    registers[instruction.c] = registers[instruction.a] * registers[instruction.b]
    return True


def halt(instruction, registers):
    return False


def execute_opcode(opcode_integers, integers):
    instruction = Instruction(*opcode_integers)
    decoder = {
        1: add,
        2: multi,
        99: halt
    }
    return decoder[instruction.opcode](instruction, integers)


def execute_intcode(integers, noun, verb):
    ints = integers.copy()
    ints[1] = noun
    ints[2] = verb

    for ip in range(0, len(ints),4):
        opcode_integers = ints[ip:ip + 4]

        # Pad with zeros if length is less than 4
        opcode_integers += [0] * (4 - len(opcode_integers))

        if not execute_opcode(opcode_integers, ints):
            break

    return ints


def find_noun_and_verb_for_output(integers, output):
    for noun in range(100):
        for verb in range(100):
            result = execute_intcode(integers, noun, verb)
            if result[0] == output:
                return 100 * noun + verb


def main():
    integers = get_integers_from_file('input.txt')
    result = execute_intcode(integers, 12, 2)
    print('Part 1 answer: {}'.format(result[0]))
    print('Part 2 answer: {}'.format(find_noun_and_verb_for_output(integers, 19690720)))
    return 0


if __name__ == '__main__':
    exit(main())
